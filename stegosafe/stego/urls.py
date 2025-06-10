from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('encode/', views.encode_view, name='encode'),
    path('decode/', views.decode_view, name='decode'),
]
