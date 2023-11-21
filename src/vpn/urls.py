from django.urls import path
from . import views

urlpatterns = [
    path('vpn/<str:site_name>/', views.proxy, name='proxy'),
    path('vpn/<str:site_name>/<path:path>/', views.proxy, name='proxy_with_path'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('', views.HomeView.as_view(), name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('create-site/', views.CreateSite.as_view(), name='create_site'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('delete-site/<int:pk>/', views.DeleteSiteView.as_view(), name='delete_site'),

    # path('<str:site_name>/<str:url>/', views.proxy, name='proxy'),
]