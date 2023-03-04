from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from authapp import models as authapp_models
from mainapp import models as mainapp_models


class TestOpenMainPage(TestCase):
    fixtures = (
        "authapp/fixtures/initial_data.json",
        "mainapp/fixtures/initial_data.json",
    )

    def test_open_page(self):
        path = reverse("mainapp:main_page")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class TestAddHouse(TestCase):
    fixtures = (
        "authapp/fixtures/initial_data.json",
        "mainapp/fixtures/initial_data.json",
    )

    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        self.user_admin = authapp_models.CustomUser.objects.get(username="ad")
        self.client_with_auth.force_login(
            self.user_admin, backend="django.contrib.auth.backends.ModelBackend"
        )

    def test_add_house(self):
        counter_before = mainapp_models.Work.objects.count()
        path = reverse("mainapp:add")
        self.address = mainapp_models.Address.objects.get(pk="1")
        self.client_with_auth.post(
            path,
            data={
                "address": "1",
            },
        )
        self.assertGreater(mainapp_models.Work.objects.count(), counter_before)
