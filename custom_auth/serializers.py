from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.urls import exceptions as url_exceptions
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer

class CustomLoginSerializer(LoginSerializer):

    def authenticate(self, **kwargs):
        email = kwargs.get('email')
        if email:
            user = get_user_model().objects.filter(email=kwargs['email']).first()
            kwargs['username'] = user.get_username()
        return authenticate(self.context['request'], **kwargs)


    def get_auth_user_using_allauth(self, username, email, password):
        from allauth.account import app_settings as allauth_account_settings
        return self._validate_username_email(username, email, password)