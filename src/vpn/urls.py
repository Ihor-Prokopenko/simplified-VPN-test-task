from django.urls import path
from . import views

urlpatterns = [
    path('<str:site_name>/', views.proxy, name='proxy'),
    # path('<str:site_name>/<str:url>/', views.proxy, name='proxy'),
]