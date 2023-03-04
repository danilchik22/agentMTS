import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model

from authapp import models

from authapp import forms


class CustomLoginView(LoginView):
    def form_valid(self, form):
        ret = super().form_valid(form)
        message = _("Яяяяяяяхаааааа бля!<br>Здаровки, %(username)s") % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Чёт не то, братан, проверь данные:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("Пока, лодырь!"))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def post(self, request, *args, **kwargs):
        try:
            if all(
                (
                    request.POST.get("username"),
                    request.POST.get("email"),
                    request.POST.get("password1"),
                    request.POST.get("password1") == request.POST.get("password2"),
                )
            ):
                new_user = models.CustomUser.objects.create(
                    username=request.POST.get("username"),
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    age=request.POST.get("age") if request.POST.get("age") else 0,
                    avatar=request.FILES.get("avatar"),
                    email=request.POST.get("email"),
                )
                new_user.set_password(request.POST.get("password1"))
                new_user.save()
                messages.add_message(
                    request, messages.INFO, _("Регистрация успешна!!!!!")
                )
                return HttpResponseRedirect(reverse_lazy("authapp:login"))
        except Exception as exp:
            messages.add_message(
                request,
                messages.WARNING,
                mark_safe(f"Регистрация не удалась. Проверь поля:<br>{exp}"),
            )
            return HttpResponseRedirect(reverse_lazy("authapp:register"))


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    template_name = "edit_user.html"
    form_class = forms.CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("mainapp:main_page")
