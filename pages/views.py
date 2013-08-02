from pages.models import Page
from django.shortcuts import render


def index(request):
    info_list = Page.objects.filter(category__exact='info')
    group_list = Page.objects.filter(category__exact='group').order_by('page_name')
    return render(request, 'pages/index.html', {'info_list': info_list,
                                                'group_list': group_list})


def info(request, info):
    info_page = Page.objects.filter(slug=info)[0]
    info_list = Page.objects.filter(category__exact='info')
    group_list = Page.objects.filter(category__exact='group').order_by('page_name')
    return render(request, 'pages/info.html', {'info_name': info_page.page_name,
                                               'description_text': info_page.description_text,
                                               'info_list': info_list,
                                               'group_list': group_list},)


def contact(request):
    return render()


def group(request, group):
    group_page = Page.objects.filter(slug=group)[0]
    group_list = Page.objects.filter(category__exact='group').order_by('page_name')
    return render(request, 'pages/group.html', {'group_name': group_page.page_name,
                                                'description_text': group_page.description_text,
                                                'group_list': group_list},)