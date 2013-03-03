from django.template import Context, loader
from django.http import HttpResponse
from pages.models import Page

def pages(request):
	band_page_info_list = Page.objects.all()
	t = loader('pages/home.html')
	c = Context({
		'band_page_info_list': band_page_info_list
		})
	return HttpResponse(t.render(c))


