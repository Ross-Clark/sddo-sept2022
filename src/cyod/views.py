from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View

from cyod.models import Product, Order, OrderItem
from cyod.forms import *

import logging


logger = logging.getLogger(__name__)

class IndexView(View):

    template_name = 'cyod.html'

    def get(self, request):

        return render(request,self.template_name)

class AllProductsView(View):

    template_name = 'products/products.html'

    def get(self,request):

        laptop = list(Product.objects.filter(product_type="lap"))
        phone = list(Product.objects.filter(product_type="pho"))
        accessory = list(Product.objects.filter(product_type="acc"))

        context = {"products":
            {
                "Laptops": laptop,
                "Phones": phone,
                "Accessories": accessory,
            }
        }

        return render(request,self.template_name,context)


class ProductView(View):

    template_name = 'products/product_page.html'

    def get(self,request,product_name):
        try:
            product = Product.objects.get(name=product_name)
        except product.DoesNotExist:
            logger.warning("product does not exist - product view")
            raise Http404("product does not exist")

        form = OrderItemForm()

        context = {
                "product" : product,
                "form":form,
            }

        return render(request,self.template_name,context)

    def post(self,request,product_name):

        user = request.user

        try:
            product = Product.objects.get(name = product_name)
        except Product.DoesNotExist:
            username = user.username
            logger.warning("Product does not exist, User:%s",username)

        form = OrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            order_type = form.cleaned_data.get('order_type')

        basket = Order.objects.filter( user = user ).filter(
            date_placed = None)

        if len(basket) == 0:
            
            basket = Order.objects.create(user=user)
            OrderItem.objects.create(
                order=basket,
                product=product,
                quantity=quantity,
                order_type=order_type
            )

        else:
            basket = basket.first()
            OrderItem.objects.create(
                    order=basket,
                    product=product,
                    quantity=quantity,
                    order_type=order_type
                )

        return redirect("choose-your-own-device/orders/basket")

class OrderHistoryView(View):

    template_name = 'orders/order_history.html'

    def get(self,request):

        try:
            user = request.user
        except:
            logger.warning("cant find user %s - order history",user.username)
        orders = Order.objects.filter(
                user=user
            ).exclude(
                date_placed=None
            )
        context = {"orders":orders}
        return render(request,self.template_name,context)

class BasketView(View):
    template_name = 'orders/order.html'

    def get(self,request,order_type,product_name):
        form = None

        return render(request,self.template_name,{'context':context})

    def post(self,request):
        form = None

        return render(request,self.template_name,{'form':form})

class OrderView(View):
    template_name = 'orders/order.html'

    def get(self,request):

        return render(request,self.template_name)
    
    def post(self,request):

        return render(request,self.template_name)

