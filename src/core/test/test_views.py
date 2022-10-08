from django.test import TestCase
from django.urls import reverse

from user import models


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_index_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_index_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)

    def test_index_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, "/user/login/")


class AboutViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        models.User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="test",
            last_name="user",
        )

    def test_about_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_about_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_about_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
