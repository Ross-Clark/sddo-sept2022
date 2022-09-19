from django.urls import path

from cyod.views import index

urlpatterns = [
    path('', index, name='index'),
]