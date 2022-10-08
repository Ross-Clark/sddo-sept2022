from tkinter import S
from django.test import TestCase
from django.contrib import auth
from django.urls import reverse

from user import models
import user


def create_user(u="testuser", p="testpass123", s=False) -> models.User:
    user = models.User.objects.create_user(
        username=u,
        password=p,
        is_staff=s,
    )
    return user


class LogoutViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        create_user()

    @classmethod
    def tearDownClass(cls):
        models.User.objects.all().delete()

    def test_logout_view_redirects_to_root(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/user/logout")
        self.assertEqual(response.status_code, 301)


class SignUpView(TestCase):
    @classmethod
    def setUpClass(cls):
        create_user()

    @classmethod
    def tearDownClass(cls):
        models.User.objects.all().delete()

    def test_signup_view_url_exists_at_desired_location(self):
        response = self.client.get("/user/signup/")
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_signup_view_url_accessible_by_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_creates_user(self):
        self.client.logout()
        response = self.client.post(
            "/user/signup/",
            {
                "username": "testuser2",
                "password1": "tasdfsAFEsdfp@sa123",
                "password2": "tasdfsAFEsdfp@sa123",
                "email": "auser@email.com",
                "first_name": "test",
                "last_name": "user",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.client.login(username="testuser2", password="tasdfsAFEsdfp@sa123")
        self.assertEqual(auth.get_user(self.client).username, "testuser2")
        self.client.logout()
        models.User.objects.get(username="testuser2")

    def test_signup_view_redirects_to_root_if_logged_in(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/choose-your-own-device/")


class TestProfileViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        create_user()

    @classmethod
    def tearDownClass(cls):
        models.User.objects.all().delete()

    def test_profile_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)

    def test_profile_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/profile.html")

    def test_profile_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/user/login/")


class EditUserViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        create_user()

    @classmethod
    def tearDownClass(cls):
        models.User.objects.all().delete()

    def test_edit_user_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/user/edit/")
        self.assertEqual(response.status_code, 200)

    def test_edit_user_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("edit_user"))
        self.assertEqual(response.status_code, 200)

    def test_edit_user_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("edit_user"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/edit_user.html")

    def test_edit_user_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("edit_user"))
        self.assertRedirects(response, "/user/login/")

    def test_edit_user_view_updates_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            "/user/edit/",
            {"first_name": "testier", "last_name": "user", "email": "2nd@email.com"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/profile/")
        self.assertEqual(auth.get_user(self.client).first_name, "testier")


class LogsViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        user = create_user(s=True)

    @classmethod
    def tearDownClass(cls):
        models.User.objects.all().delete()

    def test_logs_view_cant_be_accessed_by_non_staff(self):
        self.client.logout()
        create_user(u="testuser2", p="testpass1235")
        self.client.login(username="testuser2", password="testpass1235")
        response = self.client.get(reverse("log"))
        self.assertEqual(response.status_code, 403)
        models.User.objects.get(username="testuser2").delete()

    def test_logs_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/user/admin/logs/")
        self.assertEqual(response.status_code, 200)

    def test_logs_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("log"))
        self.assertEqual(response.status_code, 200)

    def test_logs_view_serves_log_file(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("log"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/octet-stream")
        self.assertEqual(
            response["Content-Disposition"], 'inline; filename="general.log"'
        )

    def test_logs_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("log"))
        self.assertRedirects(response, "/user/login/")
