from datetime import datetime, timedelta, date
import os
import random
import string
from PIL import Image, ImageOps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q


class MemberManager(BaseUserManager):
    """
    Custom manager for the custom Member-model used in the auth. This is
    needed to make the model work as a user. See
    https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#django.contrib.auth.models.CustomUserManager
    """
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        member = self.model(username=username, **extra_fields)
        member.set_password(password)
        member.save(self._db)
        return member

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self._create_user(username, password, **extra_fields)


def _original_photo_location(instance, filename):
    """
    Generates a file location for the profile photo of a Member provided by
    `instance`, where the original name of the file is `filename`
    """
    # TODO: Should use settings for photo paths
    return "profile_photos/original/{}.{}".format(instance.pk, filename.split(".")[-1])


def _thumb_location(instance, size):
    """
    Generates a file location for the thumbnail of a given `size` for the
    member given by `instance`
    """
    # TODO: Should use settings for path
    return "profile_photos/s_{}/{}.{}".format(size, instance.pk, "jpg")


class Member(AbstractBaseUser):
    """
    Represents a person who is a member of Lafte, storing relevant, current
    information about the person, and also serves as a Django auth-model for
    logging in. See
    https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#specifying-a-custom-user-model
    for more information on using this as the User-model.

    FUTURE WORK
    There is a lot of Låfte-specific stuff in the members-app, which should
    probably be separated out at some point. Things like is_ensemble in
    group, is_pang in member etc. Thumbnail-system could perhaps also be its
    own app.
    """
    class Meta:
        verbose_name = "medlem"
        verbose_name_plural = "medlemmer"

    username = models.CharField(max_length=255, verbose_name="brukernavn", unique=True)

    # Details needed to use this model as the auth-user-model:
    is_active = models.BooleanField(verbose_name="er aktiv", default=True)
    is_admin = models.BooleanField(verbose_name="er admin", default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = MemberManager()

    first_name = models.CharField(max_length=100, verbose_name="fornavn", blank=True)
    last_name = models.CharField(max_length=100, verbose_name="etternavn", blank=True)

    bio = models.TextField(verbose_name="om meg", blank=True)
    profile_photo = models.ImageField(upload_to=_original_photo_location, blank=True,
                                      null=True, verbose_name="profilbilde")

    # todo: interface this with http://developer.bring.com/api/postalcodeapi.html
    postal_code = models.CharField(max_length=4, verbose_name="postnummer", blank=True)
    city = models.CharField(max_length=50, verbose_name="sted", blank=True)
    address = models.TextField(blank=True, verbose_name="adresse")
    phone = models.CharField(max_length=40, verbose_name="telefonnummer", blank=True)

    email = models.EmailField(verbose_name="e-post", blank=True)

    birth_date = models.DateField(verbose_name="fødselsdato", blank=True, null=True)

    has_completed_profile = models.BooleanField(verbose_name="har fullført registrering", default=True)

    # TODO: låfte-specific info in members-app, not optimal solution
    is_pang = models.BooleanField(verbose_name="er pang", default=False)

    def get_full_name(self):
        return (self.first_name + " " + self.last_name).strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name() or self.get_username()

    def get_current_groups(self):
        """
        Gets the Groups the Member is currently a member of.
        """
        memberships = self.get_current_memberships().select_related('group')
        # TODO: This is probably not effective. Should be looked into
        return list({m.group for m in memberships})

    def get_current_memberships(self):
        """
        Gets the GroupMemberships that are current (that is has begun and
        has not ended) for the Member
        """
        return GroupMembership.get_current().filter(member=self)

    def get_membership_periods(self, include_loa=True, only_ensembles=True):
        """
        Returns a list of (start_date, end_date)-tuples representing all
        periods for which the member has been a member of any group (or any
        ensemble if only_ensembles==True). That is it will merge overlapping
        membership periods for different groups and return them as one
        continuous period in the resulting list.
        If include_loa is True, there will be a gap in the period if there
        was a LoA.
        """
        # TODO: include_loa is a stupid name
        now = date.today()
        memberships = self.memberships.filter(
            from_date__isnull=False).filter(from_date__lt=now).order_by('from_date')
        if only_ensembles:
            memberships = memberships.filter(group__is_ensemble=True)
        # Generates periods for all memberships, potentially split at LoAs
        periods = []
        for m in memberships:
            loas = m.loa_set.order_by('from_date') if include_loa else []
            start = m.from_date
            for l in loas:
                periods.append((start, min(l.from_date, now)))
                if l.to_date >= now:
                    start = now
                    break
                start = l.to_date
            if start < now:
                periods.append((start, min((m.to_date or now), now)))
        if len(periods) < 2:
            return periods
        # Merges any overlapping periods generated above
        merged = []
        saved = list(periods[0])
        for st, en in periods:
            if st <= saved[1]:
                saved[1] = min(max(saved[1], en), now)
            else:
                merged.append(tuple(saved))
                saved[0] = st
                saved[1] = min(en, now)
            if saved[1] == now:
                break
        merged.append(tuple(saved))
        return merged

    def get_total_membership_time(self, include_loa=True, only_ensembles=True):
        """
        Gets the total time this Member has been a member of some group.
        If include_loa is True, takes leaves of absence into consideration.
        If only_ensembles is True, only groups which are ensembles will be
        considered valid groups for the time total
        """
        periods = self.get_membership_periods(include_loa, only_ensembles)
        if len(periods) < 1:
            return timedelta(0)
        else:
            return sum([x[1] - x[0] for x in periods], timedelta())


    def thumb_url(self, size):
        """
        Returns the smallest thumbnail for this Member which is >= size
        """
        if not self.profile_photo:
            return None
        actual_size = min([s for s in settings.THUMB_SIZES if s >= size])
        return os.path.join(settings.MEDIA_URL, _thumb_location(self, actual_size))

    # The following three methods are required for the Model to work with the
    # built-in admin interface in Django. See
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#custom-users-and-django-contrib-admin

    def is_staff(self):
        """Used by Django admin. Returns whether Member can access admin"""
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """Used by Django admin. Returns true for now"""
        return True

    def has_module_perms(self, app_label):
        """Used by Django admin. Returns true for now"""
        return True

    # todo: Thumbs-code must be moved out of Member-class, preferably to a thumbs-field
    def generate_thumbs(self, sizes=settings.THUMB_SIZES):
        """
        Generates thumbnails from the current profile photo of the user,
        for each of the sizes given in `sizes`
        """
        pil_img = Image.open(self.profile_photo)
        for size in sizes:
            thumb = ImageOps.fit(pil_img, (size, size), Image.BICUBIC)
            path = os.path.join(settings.MEDIA_ROOT, _thumb_location(self, size))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            thumb.save(path, 'JPEG')
        os.remove(self.profile_photo.path)
        self.profile_photo = _thumb_location(self, max(sizes))

    def save(self, *args, **kwargs):
        super(Member, self).save(*args, **kwargs)
        # If we have changed the photo, we should generate new thumbs
        # TODO: profile-photo-path in settings
        if self.profile_photo and self.profile_photo.name.startswith('profile_photos/original'):
            self.generate_thumbs()
            super(Member, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('members:member', args=[self.pk])

    # TODO: Again, Låfte mangled in with members
    @staticmethod
    def get_potential_pangs():
        """
        Gets potential pangs, by virtue of having been more than 2,5 years
        (i.e. 6 semesters) at Låfte. Also annotates the members with total
        semesters and total days they have been a member
        """
        for m in Member.objects.filter(is_pang=False, is_active=True):
            days = m.get_total_membership_time().days
            if days > 365*2.5:
                m.days = days
                m.semesters = days//(365//2)
                yield m


class Group(models.Model):
    """
    Represents an organization unit of members, both ensembles and other real
    life groups, and other collections accross members that are needed. Will
    in the future probably be used for access control for documents etc.
    """
    class Meta:
        verbose_name = "gruppe"
        verbose_name_plural = "grupper"

    name = models.CharField(max_length=60, verbose_name="navn")
    description = models.TextField(blank=True, verbose_name="beskrivelse")
    # TODO: Låfte specific. Should be extracted
    is_ensemble = models.BooleanField(default=False, verbose_name="gruppering",
                                      help_text="Gruppen er en gruppering på Låfte")
    hidden = models.BooleanField(default=False, verbose_name="skjult")
    members = models.ManyToManyField(Member, through='GroupMembership')

    def get_current_memberships(self):
        """
        Gets the memberships that are current, i.e. have started and not
        ended
        """
        return GroupMembership.get_current().filter(group=self)

    def get_current_members(self):
        # todo: optimize this, probably (do db-stuff instead of set-comprehension)
        return list({m.member for m in self.get_current_memberships()})

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    """
    Represents a connection between a Member and a Group, with a to_date and
    a from_date for storing historical data, to signify that the member was
    a member of the given group in the given time span. If a time span is not
    available, the dates may be null, which is interpreted as from and to
    infinity, respectively.
    """
    class Meta:
        verbose_name = "gruppemedlemskap"
        verbose_name_plural = "gruppemedlemskap"

    member = models.ForeignKey(Member, verbose_name="medlem", related_name="memberships")
    group = models.ForeignKey(Group, verbose_name="gruppe", related_name="memberships")
    from_date = models.DateField(blank=True, null=True, verbose_name="fra dato")
    to_date = models.DateField(blank=True, null=True, verbose_name="til dato")
    description = models.TextField(blank=True, verbose_name="beskrivelse")

    @staticmethod
    def get_current():
        """
        Gets the memberships that have started AND not ended yet
        """
        now = datetime.today()
        q = (Q(to_date__gt=now) | Q(to_date__isnull=True)) & \
            (Q(from_date__lt=now) | Q(from_date__isnull=True))
        return GroupMembership.objects.filter(q)

    def __str__(self):
        return "{} medlem av {} ({} - {})".format(
            self.member.get_full_name(), self.group.name,
            self.from_date if self.from_date is not None else '',
            self.to_date if self.to_date is not None else '')


class LoA(models.Model):
    """
    A leave of absence from a GroupMembership, represented by the time span of
    the leave
    """
    class Meta:
        verbose_name = "permisjon"
        verbose_name_plural = "permisjoner"

    membership = models.ForeignKey(GroupMembership, verbose_name="medlemskap")
    from_date = models.DateField(verbose_name="fra dato")
    to_date = models.DateField(verbose_name="til dato")
    reason = models.TextField(blank=True, verbose_name="årsak")

    def __str__(self):
        return "{} permittert fra {} ({} - {})".format(
            self.membership.member.get_full_name(), self.membership.group.name, self.from_date, self.to_date)


class Position(models.Model):
    """
    Data about a specific position a member holds in a group, represented
    by the title of the position and a time span. If the from_date or to_date
    are null, the dates from the associated GroupMembership should be used
    instead
    """
    class Meta:
        verbose_name = "stilling"
        verbose_name_plural = "stillinger"

    membership = models.ForeignKey(GroupMembership, verbose_name="medlemskap", related_name="positions")
    title = models.CharField(max_length=60, verbose_name="tittel")
    from_date = models.DateField(blank=True, null=True, verbose_name="fra dato")
    to_date = models.DateField(blank=True, null=True, verbose_name="til dato")
    description = models.TextField(blank=True, verbose_name="beskrivelse")

    def __str__(self):
        return "{} som {} i {} ({} - {})".format(
            self.membership.member.get_full_name(), self.title, self.membership.group.name,
            self.from_date, self.to_date)