from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Urls


class ProjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_data = Urls.objects.create(
            short_url="TESTSTR1",
            long_url="https://github.com/mmleonowicz/url_shortener",
        )
        test_data.save()

    def test_model_content(self):
        test_url = Urls.objects.get(id=1)
        short_url = f"{test_url.short_url}"
        long_url = f"{test_url.long_url}"
        self.assertEqual(short_url, "TESTSTR1")
        self.assertEqual(long_url, "https://github.com/mmleonowicz/url_shortener")


class ApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_data = Urls.objects.create(
            short_url="TESTSTR1",
            long_url="https://github.com/mmleonowicz/url_shortener",
        )
        test_data.save()

    def test_response_status_code(self):
        test_ip = {"long_url": "https://github.com/mmleonowicz/url_shortener"}
        response = self.client.post(reverse("shorten"), test_ip, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_content(self):
        test_ip = {"long_url": "https://github.com/mmleonowicz/url_shortener"}
        response = self.client.post(reverse("shorten"), test_ip, format="json")
        self.assertEqual(
            response.data["long_url"], "https://github.com/mmleonowicz/url_shortener"
        )

    def test_redirect(self):
        response = self.client.get(
            reverse("redirect_short", kwargs={"short_url": "TESTSTR1"})
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "https://github.com/mmleonowicz/url_shortener")

    def test_not_found(self):
        response = self.client.get(
            reverse("redirect_short", kwargs={"short_url": "not_found"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
