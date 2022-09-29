from django.urls import path

from cyod import views


app_name= 'cyod'
urlpatterns = [
    #/choose-your-own-device
    path('', views.IndexView.as_view(), name='index'),
    #/choose-your-own-device/product/<int>
    path('products/',views.AllProductsView.as_view(), name='all_products'),
    #/choose-your-own-device/products/<int>
    path('products/<str:product_name>',views.ProductView.as_view(), name='product'),
    #/choose-your-own-device/order/
    path('order/',views.OrderView.as_view(), name='order'),
    #/choose-your-own-device/order-history/
    path('order-history/',views.OrderHistoryView.as_view(), name='order_history'),
    #/choose-your-own-device/basket/
    path('basket/',views.BasketView.as_view(), name='order_history'),
]