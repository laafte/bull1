from pages.models import Page
from django.shortcuts import render


def index(request):
    group_list = Page.objects.filter(category__exact='group').order_by('page_name')
    return render(request, 'pages/index.html', {'group_list': group_list})


def info(request):
    return render()


def contact(request):
    return render()


def group(request, group):
    group_page = Page.objects.filter(slug=group)[0]
    group_list = Page.objects.filter(category__exact='group').order_by('page_name')
    return render(request, 'pages/group.html', {'group_name': group_page.page_name,
                                                'description_text': group_page.description_text,
                                                'group_list': group_list},)