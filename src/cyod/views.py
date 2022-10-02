from datetime import datetime
from django.http import Http404
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, Http404
from django.views import View

from cyod import forms
from cyod.models import Product, Order, OrderItem

import logging


logger = logging.getLogger(__name__)


class IndexView(View):

    template_name = "cyod.html"

    def get(self, request):

        return render(request, self.template_name)


class AllProductsView(View):

    template_name = "products/products.html"

    def get(self, request):

        laptop = list(Product.objects.filter(product_type="lap"))
        phone = list(Product.objects.filter(product_type="pho"))
        accessory = list(Product.objects.filter(product_type="acc"))

        context = {
            "products": {
                "Laptops": laptop,
                "Phones": phone,
                "Accessories": accessory,
            }
        }

        return render(request, self.template_name, context)


class ProductView(View):

    template_name = "products/product_page.html"

    def get(self, request, product_name):
        try:
            product = Product.objects.get(name=product_name)
        except product.DoesNotExist:
            logger.warning("product does not exist - product view")
            raise Http404("product does not exist")

        form = forms.OrderItemProductViewForm()

        context = {
            "product": product,
            "form": form,
        }

        return render(request, self.template_name, context)

    def post(self, request, product_name):

        user = request.user

        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            username = user.username
            logger.warning("Product does not exist, User:%s", username)

        form = forms.OrderItemProductViewForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get("quantity")
            order_type = form.cleaned_data.get("order_type")

        basket = Order.objects.filter(user=user).filter(date_placed=None)

        # if unplaced order does not exist make one
        # and populate it with the OrderItem
        if len(basket) == 0:

            basket = Order.objects.create(user=user)
            OrderItem.objects.create(
                order=basket, product=product, quantity=quantity, order_type=order_type
            )

        else:
            basket = basket.first()
            OrderItem.objects.create(
                order=basket, product=product, quantity=quantity, order_type=order_type
            )

        return redirect("/choose-your-own-device/basket")


class OrderHistoryView(View):

    template_name = "orders/order_history.html"

    def get(self, request):

        try:
            user = request.user
        except:
            logger.warning("cant find user %s - order history", user.username)
        orders = Order.objects.filter(user=user).exclude(date_placed=None)
        context = {"orders": orders}
        return render(request, self.template_name, context)


class BasketView(View):

    template_name = "orders/basket.html"

    basketFormset = modelformset_factory(
        OrderItem, forms.BasketForm, can_delete=True, extra=0
    )

    def get(self, request):

        basket = get_basket_order_queryset(request)

        # if unplaced order does not exist return no items in basket
        # else return formset of all orderitems
        if len(basket) == 0:
            return render(request, self.template_name, {"form": None})
        else:
            basket = get_basket_order(request)

            # create formset for orderitems in order
            Formset = self.basketFormset(queryset=basket.OrderItem.all())

            # set product name related to orderitem
            Formset = self.get_product_name(Formset)

            return render(request, self.template_name, {"formset": Formset})

    def post(self, request):

        Formset = self.basketFormset(request.POST)

        Formset = self.get_product_name(Formset)

        # if submit type is wrong raise error
        submitType = request.POST.get("submit")
        if submitType not in ["Submit Changes", "Complete Order"]:
            # raises error and displays error page
            logger.warning(
                "unsupported submit name in basket form user:%s", request.user.username
            )
            raise Http404("<h1> suspicious operation </h1>")

        if Formset.is_valid():
            Formset.save()
        else:
            return render(request, self.template_name, {"formset": Formset})

        if submitType == "Complete Order":
            # redirect to order page

            return redirect("/choose-your-own-device/order")

        elif submitType == "Submit Changes":
            # redisplays the updated page
            # has to refresh the formset
            basket = get_basket_order(request)
            Formset = self.basketFormset(queryset=basket.OrderItem.all())
            Formset = self.get_product_name(Formset)
            return render(request, self.template_name, {"formset": Formset})

    def get_product_name(self, basketFormset):
        for form in basketFormset:
            product = Product.objects.get(id=form.instance.product_id).name
            form.initial["product_name"] = product
        return basketFormset


class OrderView(View):
    template_name = "orders/order.html"

    def get(self, request):

        basket = get_basket_order_queryset(request)
        # prevent empty or non existant baskets from being accessed
        if basket == None or not basket.values("OrderItem").first().get(
            "OrderItem", None
        ):
            logger.warning(
                "user:%s tried to access order view without basket",
                request.user.username,
            )
            return redirect("/choose-your-own-device/basket")
        basket = basket.first()
        form = forms.OrderForm(instance=basket)

        return render(request, self.template_name, {"form": form})

    def post(self, request):

        # check that the order has order items
        basket = get_basket_order_queryset(request)
        if not basket.values("OrderItem").first().get("OrderItem", None):
            logger.warning(
                "user:%s tried to access order view without orderItems",
                request.user.username,
            )
            return redirect("/choose-your-own-device/basket")

        # initiate instance of form
        basket = basket.first()
        form = forms.OrderForm(request.POST, instance=basket)

        # validate form, add date_placed and status then save to db
        if form.is_valid():
            order = form.save(commit=False)
            order.date_placed = datetime.now().strftime("%Y-%m-%d")
            order.status = "wait"
            order.save()
            logger.info(
                "user:%s made order order_id:%s", request.user.username, order.pk
            )
            return redirect("/choose-your-own-device/order/confirmed")
        else:
            return render(request, self.template_name, {"form": form})


class OrderConfirmView(View):
    template_name = "orders/confirmation.html"

    def get(self, request):

        return render(request, self.template_name)


def get_basket_order_queryset(request):

    user = request.user

    return Order.objects.filter(user=user).filter(date_placed=None)


def get_basket_order(request):
    basket = get_basket_order_queryset(request).first()
    return basket
