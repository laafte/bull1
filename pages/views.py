from django.http.response import HttpResponse
from pages.models import Page, Category
from django.shortcuts import render


def index(request):
    group_list = Page.objects.filter(category__category_name='Groups')
    return render(request, 'pages/index.html', {'group_list': group_list})


def info(request):
    return render()


def contact(request):
    return render()


def group(request, group):
    return HttpResponse('ok')