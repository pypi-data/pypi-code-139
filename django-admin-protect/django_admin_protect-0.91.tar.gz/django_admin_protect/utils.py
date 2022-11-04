from django.http import Http404
from django.shortcuts import redirect
from django.core.mail import EmailMessage

from .apps import DjangoAdminProtectConfig

import random
import importlib
from datetime import datetime, timedelta


DEFAULT_SETTINGS = DjangoAdminProtectConfig.DEFAULT_SETTINGS
SETTINGS = DjangoAdminProtectConfig.SETTINGS


def token_required(func):
    def wrapper(request, token=None, *args, **kwargs):
        need_token = SETTINGS.get("UPDATE_ADMIN_PATH", {}).get("INCLUDING") or DEFAULT_SETTINGS["UPDATE_ADMIN_PATH"]["INCLUDING"]
        if need_token and not token:
            raise Http404

        if not need_token and token:
            return redirect("django_admin_protect_login")

        return func(request, token=token, *args, **kwargs)
    
    return wrapper


def get_token(*args, **kwargs):
    if generator := SETTINGS.get("OTP", {}).get("GENERATOR"):
        if func := importlib.import_module(generator):
            return func()
    
    token_width = SETTINGS.get("OTP", {}).get("WIDTH") or DEFAULT_SETTINGS["OTP"]["WIDTH"]
    return ''.join(map(str, random.choices(range(0, 10), k=token_width)))


def get_dt_issued(*args, **kwargs):
    if dt_issued := SETTINGS.get("OTP", {}).get("DATE_ISSUED"):
        return datetime.now() + timedelta(seconds=dt_issued)
    
    dt_issued = DEFAULT_SETTINGS["OTP"]["DATE_ISSUED"]
    return datetime.now() + timedelta(seconds=dt_issued)


def send_otp(admin_protect):
    title = SETTINGS.get("OTP", {}).get("MESSAGE_TITLE") or DEFAULT_SETTINGS["OTP"]["MESSAGE_TITLE"]
    body = (SETTINGS.get("OTP", {}).get("MESSAGE_BODY") or DEFAULT_SETTINGS["OTP"]["MESSAGE_BODY"]) % admin_protect.token
    mail_fields = SETTINGS.get("OTP", {}).get("MAIL_FIELDS") or DEFAULT_SETTINGS["OTP"]["MAIL_FIELDS"]

    for field in mail_fields:
        if hasattr(admin_protect.user, field) and (mail := getattr(admin_protect.user, field)):
            return EmailMessage(
                subject=title,
                body=body,
                to=[mail]
            ).send()

