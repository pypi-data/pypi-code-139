from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AdminProtectForm(AuthenticationForm):
    def __init__(self, admin_protect=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control form-control-sm text-center", "placeholder": "Username"}
        )

        self.fields["password"].widget.attrs.update(
            {"class": "form-control form-control-sm text-center", "placeholder": "Password"}
        )

        if admin_protect:
            del self.fields["username"]
            del self.fields["password"]

            self.fields["otp"] = forms.CharField(
                required=False,
                widget=forms.TextInput({
                    "class": "form-control form-control-sm text-center",
                    "placeholder": "One Time Password"
                })
            )

            self.admin_protect = admin_protect
            self.user = self.admin_protect.user
