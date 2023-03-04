from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("addhouse/", views.AddHousePage.as_view(), name="add"),
    path("list_houses/", views.ListHousePage.as_view(), name="list_houses"),
    path("padiki/", views.PadikiPage.as_view(), name="padiki"),
    path("log_view/", views.LogView.as_view(), name="log"),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),
    path("support/", views.SupportView.as_view(), name="support"),
]
