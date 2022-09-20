from django.urls import path

from cyod import views


app_name= 'cyod'
urlpatterns = [
    #/choose-your-own-device
    path('', views.IndexView.as_view(), name='index'),
    #/choose-your-own-device/product/<int>
    path('product/<str:product_name>',views.product, name='product'),
    #/choose-your-own-device/order/
    path('choose-your-own-device/order',views.order, name='order')
]