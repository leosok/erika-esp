from allauth.account.forms import ResetPasswordForm
from django.conf.global_settings import AUTH_USER_MODEL
from django.http import HttpRequest

from erika_cloud import settings


def send_password_reset(user: AUTH_USER_MODEL):
    request = HttpRequest()
    request.user = user
    request.META["HTTP_HOST"] = settings.HTTP_HOST

    form = ResetPasswordForm({"email": user.email})
    if form.is_valid():
        form.save(request)