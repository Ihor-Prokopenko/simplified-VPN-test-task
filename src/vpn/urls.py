from django.urls import path
from . import views

home = [
    path('', views.HomeView.as_view(), name='home'),
]

proxy = [
    path('vpn/<str:site_name>/', views.proxy, name='proxy'),
    path('vpn/<str:site_name>/<path:path>/', views.proxy, name='proxy_with_path'),
]

auth = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
]

sites = [
    path('create-site/', views.CreateSite.as_view(), name='create_site'),
    path('delete-site/<int:pk>/', views.DeleteSiteView.as_view(), name='delete_site'),
]

user_profile = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
]

urlpatterns = [] + home + proxy + auth + sites + user_profile
