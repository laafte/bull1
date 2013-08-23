from pages.models import Page


def group_list(request):
    group_list = Page.objects.filter(category__exact='group').order_by('page_name')
    return {'group_list': group_list}