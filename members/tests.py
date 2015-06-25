from datetime import datetime, timedelta
from django.test import TestCase
from members.models import Member, Group, GroupMembership


class MemberTestCase(TestCase):
    def setUp(self):
        Member.objects.create_superuser("super", "Super", "User", "surrehue123")
        Member.objects.create_user("bruker", "Ole", "Olsen", "passord")

    def test_authentication(self):
        superuser = Member.objects.get(username="super")
        regular_user = Member.objects.get(username="bruker")
        self.assertTrue(superuser.check_password("surrehue123"))
        self.assertFalse(superuser.check_password("feil"))
        self.assertTrue(regular_user.check_password("passord"))

    def test_admin_flag(self):
        superuser = Member.objects.get(username="super")
        regular_user = Member.objects.get(username="bruker")
        self.assertTrue(superuser.is_admin)
        self.assertFalse(regular_user.is_admin)


class CurrentGroupsAndMembershipsTestCase(TestCase):

    def setUp(self):
        m = Member.objects.create_user("br", "Ole", "Olsen", "passord")
        g1 = Group.objects.create(name="gruppe1")
        g2 = Group.objects.create(name="gruppe2")
        g3 = Group.objects.create(name="gruppe3")
        g4 = Group.objects.create(name="gruppe4")
        today = datetime.today()
        future = today + timedelta(days=100)
        past = today - timedelta(days=100)
        GroupMembership.objects.create(group=g1, member=m)
        GroupMembership.objects.create(group=g2, member=m, from_date=future)
        GroupMembership.objects.create(group=g1, member=m, to_date=past)
        GroupMembership.objects.create(group=g3, member=m, from_date=past)
        GroupMembership.objects.create(group=g4, member=m, from_date=past, to_date=future)

    def test_current_groups(self):
        m = Member.objects.get(username="br")
        grs = m.get_current_groups()
        g1 = Group.objects.get(name="gruppe1")
        g2 = Group.objects.get(name="gruppe2")
        g3 = Group.objects.get(name="gruppe3")
        g4 = Group.objects.get(name="gruppe4")
        self.assertTrue(g1 in grs)
        self.assertFalse(g2 in grs)
        self.assertTrue(g3 in grs)
        self.assertTrue(g4 in grs)

    def test_current_memberships(self):
        m = Member.objects.get(username="br")
        ms = m.get_current_memberships()
        self.assertEqual(len(ms), 3)

