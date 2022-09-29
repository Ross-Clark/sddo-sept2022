from django.http import Http404
from django.forms import formset_factory
from django.shortcuts import render, redirect, Http404
from django.views import View

from cyod import forms
from cyod.models import Product, Order, OrderItem

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

        form = forms.OrderItemForm()

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

        form = forms.OrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            order_type = form.cleaned_data.get('order_type')

        basket = Order.objects.filter( user = user ).filter(
            date_placed = None)

        # if unplaced order does not exist make one
        # and populate it with the OrderItem
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

        return redirect("/choose-your-own-device/basket")

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
    template_name = 'orders/basket.html'

    def get(self,request):

        user = request.user

        basket = Order.objects.filter( user = user ).filter(
        date_placed = None)

        # if unplaced order does not exist
        # return no items in basket
        if len(basket) == 0:
            return render(request,self.template_name,{'form':None})
        else:
            basket = basket.first()
        
        basket = list(basket.OrderItem.all())
        formset = formset_factory(forms.BasketForm, extra=0)
        basketFormset = formset(initial=
            [
                {
                    'product_name':x.product.name,
                    'quantity':x.quantity,
                    'order_type':x.order_type
                } for x in basket 
            ]
        )

        return render(request,self.template_name,{'formset':basketFormset})

    def post(self,request):
        basketFormset = None
        if 'submit' in request.POST:
            # save changes then redisplays the page
            return render(request,self.template_name,{'formset':basketFormset})
        elif 'complete' in request.POST:
            # save changes then redirect to order page
            return redirect('/choose-your-own-device/order')
        else:
            # raises error and displays error page
            logger.warning("unsupported submit name in basket form user:%s",request.user.username)
            raise Http404('<h1> suspicious operation </h1>')


class OrderView(View):
    template_name = 'orders/order.html'

    def get(self,request):

        return render(request,self.template_name)
    
    def post(self,request):

        return render(request,self.template_name)
