from django.http import HttpResponse
from django.views import View

class IndexView(View):
    template_name = 'cyod.html'
    def get(self):

        return HttpResponse("Hello, world. You're at the products index.")


def product(request, product_name):
    return HttpResponse("You're looking at %s." % product_name)

def order(request):
    return HttpResponse('hello')

