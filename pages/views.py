from pages.models import Page
from django.shortcuts import render


def index(request):
    return render(request, 'pages/index.html')


def info(request):
    info_list = Page.objects.filter(category__exact='info')
    return render(request, 'pages/info.html', {'info_list': info_list, },)


def contact(request):
    return render()


def group(request, group):
    group_page = Page.objects.filter(slug=group)[0]
    group_list = Page.objects.filter(category__exact='group').order_by('page_name')
    return render(request, 'pages/group.html', {'group_name': group_page.page_name,
                                                'description_text': group_page.description_text},)