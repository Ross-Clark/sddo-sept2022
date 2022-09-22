from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

class IndexView(View):

    template_name = 'cyod.html'

    def get(self, request):

        return render(request,self.template_name)


def product(request, product_name):
    return HttpResponse("You're looking at %s." % product_name)

def order(request):
    return HttpResponse('hello')

