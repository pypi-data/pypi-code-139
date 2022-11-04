from django.db import models
from django.contrib.auth import get_user_model

from . import utils


class AdminProtectUserAuth(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="admin_protect_auths")
    token = models.TextField(default=utils.get_token)
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_issued = models.DateTimeField(default=utils.get_dt_issued)
    dt_auth = models.DateTimeField(blank=True, null=True, default=None)
