from django.test import testcases
from user import forms, models


class CustomUserCreationFormTest(testcases.TestCase):
    def setup_user_form(self):
        form = forms.CustomUserCreationForm(
            data={
                "username": "test",
                "password1": "UniqueP@s$w0rd123",
                "password2": "UniqueP@s$w0rd123",
                "first_name": "test",
                "last_name": "test",
                "email": "email@address.com",
            }
        )
        return form

    def test_user_form_valid_data_accepted(self):
        form = self.setup_user_form()
        self.assertEquals(form.errors, {})

    def test_password_throws_error_when_not_unique(self):
        form = self.setup_user_form()
        form.data["password1"] = "password"
        form.data["password2"] = "password"
        self.assertEquals(form.errors["password2"], ["This password is too common."])

    def test_password_throws_error_when_too_short(self):
        form = self.setup_user_form()
        form.data["password1"] = "pI@s$"
        form.data["password2"] = "pI@s$"
        self.assertEquals(
            form.errors["password2"],
            ["This password is too short. It must contain at least 8 characters."],
        )

    def test_password_throws_error_when_only_numeric(self):
        form = self.setup_user_form()
        form.data["password1"] = "26545668"
        form.data["password2"] = "26545668"
        self.assertEquals(
            form.errors["password2"], ["This password is entirely numeric."]
        )

    def test_first_name_required(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("first_name").required, True)

    def test_first_name_max_length(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("first_name").max_length, 30)

    def test_last_name_required(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("last_name").required, True)

    def test_last_name_max_length(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("last_name").max_length, 30)

    def test_email_required(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("email").required, True)

    def test_email_max_length(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("email").max_length, 254)

    def test_email_throws_error_when_invalid(self):
        form = self.setup_user_form()
        form.data["email"] = "emailaddress.com"
        self.assertEquals(form.errors["email"], ["Enter a valid email address."])

    def test_username_throws_error_when_not_unique(self):
        form = self.setup_user_form()
        models.User.objects.create_user(
            username="test",
            password="UniqueP@s$w0rd123",
        )
        form.data["username"] = "test"
        self.assertEquals(
            form.errors["username"], ["A user with that username already exists."]
        )
        models.User.objects.all().delete()


class UpdateUserFormTest(testcases.TestCase):
    def setup_user_form(self):
        form = forms.UpdateUserForm(
            data={"first_name": "test", "last_name": "test", "email": "user@email.com"}
        )
        return form

    def test_first_name_required(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("first_name").required, True)

    def test_first_name_max_length(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("first_name").max_length, 30)

    def test_last_name_required(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("last_name").required, True)

    def test_last_name_max_length(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("last_name").max_length, 30)

    def test_email_required(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("email").required, True)

    def test_email_max_length(self):
        form = self.setup_user_form()
        self.assertEqual(form.base_fields.get("email").max_length, 254)

    def test_email_throws_error_when_invalid(self):
        form = self.setup_user_form()
        form.data["email"] = "emailaddress.com"
        self.assertEquals(form.errors["email"], ["Enter a valid email address."])
