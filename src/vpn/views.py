from urllib.parse import urlparse, urljoin

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View, UpdateView

from vpn.forms import SignUpForm, LoginUserForm, CreateSiteForm, EditProfileForm
from vpn.mixins import NotAuthenticatedMixin
from vpn.models import Site
from vpn.utils import replace_links


@login_required
def proxy(request, site_name, path=''):
    try:
        site = request.user.sites.get(name=site_name)
    except Site.DoesNotExist:
        messages.error(request, 'Site not found')
        return redirect('profile')

    if not site or not site.base_url:
        messages.error(request, 'Site not found')
        return redirect('profile')

    base_url = site.base_url

    parsed_url = urlparse(base_url)
    base_site_domain = parsed_url.netloc.replace("www.", "")

    request_url = urljoin(base_url, path)
    try:
        response = requests.get(request_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error: {e}')
        return redirect('profile')

    content = replace_links(response.content, site_name, site.base_url, base_site_domain, path)
    site.transitions_count += 1
    site.data_volume += len(content)
    site.save()

    return HttpResponse(content)


@login_required
def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')


class RegisterUser(NotAuthenticatedMixin, CreateView):
    form_class = SignUpForm
    template_name = 'register.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.error(self.request, "You have been registered!")
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(self.request, error)


class LoginUser(NotAuthenticatedMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and "vpn" in next_url:
            url = urljoin(settings.BASE_HOST_URL, next_url)
            return url
        url = reverse('home')
        messages.success(self.request, "You have been logged in!")
        return url


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class CreateSite(CreateView):
    form_class = CreateSiteForm
    template_name = 'create_site.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user

        if form.is_valid():
            messages.success(self.request, "Site created!")
            return super().form_valid(form)
        else:
            for error in list(form.errors.values()):
                messages.error(self.request, error)
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class DeleteSiteView(View):
    def get(self, request, pk):
        try:
            site = request.user.sites.get(pk=pk)
        except Site.DoesNotExist:
            messages.error(self.request, "Site not found!")
            return redirect('profile')
        # site = request.user.sites.get(pk)
        site_name = site.name
        deleted_count, data = site.delete()
        if not deleted_count:
            messages.error(self.request, "Site not found!")
            return redirect('profile')
        messages.success(self.request, f"Site '{site_name}' deleted!")
        return redirect('profile')
