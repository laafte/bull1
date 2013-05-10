from pages.models import Page, Category
from django.shortcuts import render


def pages(request):
    band_page_info_list = Page.objects.all()
    category_list = Category.objects.all()
    return render(request, 'pages/index.html', {'band_page_info_list': band_page_info_list,
                                                'category_list': category_list})