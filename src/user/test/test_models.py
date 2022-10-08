from django.test import TestCase

from user import models

class user_models_test(TestCase):
    def test_user_models(self):
        user = models.User.objects.create_user(
            username='test',
            password='UniqueP@s$w0rd123',
        )
        self.assertIsInstance(user, models.User)
        self.assertEqual(user.username, 'test')
        models.User.objects.all().delete()