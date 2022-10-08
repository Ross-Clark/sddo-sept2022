from django.test import testcases


class MiddlewareTest(testcases.TestCase):
    def test_login(self):
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)

    def test_restricted_page(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 301)

    def test_registration(self):
        response = self.client.get("/user/signup/")
        self.assertEqual(response.status_code, 200)
