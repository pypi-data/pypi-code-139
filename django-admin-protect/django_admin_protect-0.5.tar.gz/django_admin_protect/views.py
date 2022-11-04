from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.utils.decorators import method_decorator

from datetime import datetime

from .forms import AdminProtectForm
from .apps import DjangoAdminProtectConfig
from .models import AdminProtectUserAuth
from .utils import token_required, send_otp


@method_decorator(token_required, name="dispatch")
class AdminProtectView(FormView):
    template_name = "django_admin_protect/login.html"
    form_class = AdminProtectForm

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("back") and self.request.session.get("admin_protect_id"):
            del self.request.session["admin_protect_id"]
            return redirect("django_admin_protect_login")

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["SETTINGS"] = DjangoAdminProtectConfig.SETTINGS

        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if admin_protect_id := self.request.session.get("admin_protect_id"):
            admin_protect = AdminProtectUserAuth.objects.get(id=admin_protect_id)

            if admin_protect.dt_issued >= timezone.now():
                kwargs["admin_protect"] = admin_protect

        return kwargs
    
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        otp = form.cleaned_data.get("otp")

        if username and password:
            user = authenticate(request=self.request, username=username, password=password)
            
            if user is not None:
                admin_protect = AdminProtectUserAuth.objects.create(user=user)
                self.request.session["admin_protect_id"] = admin_protect.id

                sended = None

                try:
                    sended = send_otp(admin_protect)
                except: pass

                if not sended:
                    del self.request.session["admin_protect_id"]

                    form.errors["otp"] = ["OTP not sended"]
                    return super().form_invalid(form)

        
        elif otp and hasattr(form, "admin_protect"):
            if form.admin_protect.token == otp:
                form.admin_protect.dt_auth = datetime.now()
                form.admin_protect.save()

                login(request=self.request, user=form.admin_protect.user)

                return redirect("admin:index")
            
            form.errors["otp"] = ["Not valid OTP"]
            return super().form_invalid(form)
        
        return redirect("django_admin_protect_login")
