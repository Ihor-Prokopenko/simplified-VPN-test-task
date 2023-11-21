from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url, redirect


class NotAuthenticatedMixin(UserPassesTestMixin):
    """
    A mixin that redirects to the login page if the user is not authenticated.
    """
    def test_func(self):
        return not self.request.user.is_authenticated

    def get_login_url(self):
        return resolve_url('home')

    def get_redirect_field_name(self):
        return REDIRECT_FIELD_NAME

    def handle_no_permission(self):
        return redirect(self.get_login_url())
