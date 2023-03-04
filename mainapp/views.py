from ast import Dict
import logging
from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from mainapp import models as mainapp_models
from authapp import models as authapp_models
from django.views.generic import ListView, CreateView, View
from django.db.models import Q
from mainapp.forms import CreateWorkForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.conf import settings
from .forms import SupportForm
from django.views.generic.edit import FormView
from django.core.cache import cache
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from mainapp import tasks as mainapp_tasks


logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class ListHousePage(ListView):
    model = mainapp_models.Work
    paginate_by = 20

    def get_queryset(self):  # новый
        query = self.request.GET.get("q")
        if query is not None:
            object_list = mainapp_models.Work.objects.filter(
                Q(address__street__name_street__icontains=query) & Q(is_deleted=False)
            ).order_by("-created_at")
        else:
            object_list = mainapp_models.Work.objects.all().order_by("-created_at")
        return object_list


class AddHousePage(LoginRequiredMixin, CreateView):
    model = mainapp_models.Work
    form_class = CreateWorkForm
    success_url = reverse_lazy("mainapp:add")

    def form_valid(self, form):
        new_house = form.save(commit=False)
        new_house.user = self.request.user
        new_house.save()
        return super().form_valid(form)


class PadikiPage(TemplateView):
    template_name = "mainapp/padiki.html"


class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:  # first 1000 lines
                    break
                log_slice.insert(0, line)  # append at start
            context["log"] = "".join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))


class SupportView(TemplateView):
    template_name = "mainapp/support.html"

    def get_context_data(self, success=0, **kwargs: Any):
        context = super(SupportView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = SupportForm(user=self.request.user)
            context["success"] = success
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(f"mail_feedback_lock_{self.request.user.pk}")
            if not cache_lock_flag:
                cache.set(
                    f"mail_feedback_lock_{self.request.user.pk}",
                    "lock",
                    timeout=300,
                )
                messages.add_message(self.request, messages.INFO, _("Message sended"))
                mainapp_tasks.send_feedback_mail.delay(
                    {
                        "id_from": self.request.POST.get("id_from"),
                        "topic": self.request.POST.get("topic"),
                        "message": self.request.POST.get("message"),
                    }
                )
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _("You can send only one message per 5 minutes"),
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:support"))
