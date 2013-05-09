from pages.models import Page
from django.shortcuts import render


def pages(request):
    band_page_info_list = Page.objects.all()
    return render(request, 'pages/index.html', {'band_page_info_list': band_page_info_list})