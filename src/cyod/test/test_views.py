from datetime import datetime
import os
from django.conf import settings

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import testcases
from django.urls import reverse


from cyod import models
from user import models as user_models


def create_user():
    user_models.User.objects.create_user(username="testuser", password="testpass123")


class IndexViewTest(testcases.TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user()

    def test_index_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_index_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)

    def test_index_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, "/user/login/")


class AllProductViewTest(testcases.TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user()

    def test_all_product_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/choose-your-own-device/products/")
        self.assertEqual(response.status_code, 200)

    def test_all_product_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:all_products"))
        self.assertEqual(response.status_code, 200)

    def test_all_product_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:all_products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_all_product_view_uses_correct_context(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:all_products"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.context)


class ProductViewTest(testcases.TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user()

        models.Product.objects.create(
            name="iphone",
            product_type="pho",
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"mock image", content_type="image/jpeg"
            ),
            release=datetime.now(),
            description="test",
            roles_allowed="all",
        )

    @classmethod
    def tearDownClass(cls):
        product = models.Product.objects.get(name="iphone")
        os.remove(os.path.join(settings.MEDIA_ROOT, product.image.name))
        super().tearDownClass()

    def test_product_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/choose-your-own-device/products/iphone")
        self.assertEqual(response.status_code, 200)

    def test_product_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:product", args=["iphone"]))
        self.assertEqual(response.status_code, 200)

    def test_product_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:product", args=["iphone"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_page.html")

    def test_product_view_uses_correct_context(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:product", args=["iphone"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("product", response.context)

    def test_product_view_returns_404_if_product_does_not_exist(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:product", args=["nonexistent"]))
        self.assertEqual(response.status_code, 404)


class OrderHistoryViewTest(testcases.TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user()

    def test_order_history_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/choose-your-own-device/order-history/")
        self.assertEqual(response.status_code, 200)

    def test_order_history_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:order_history"))
        self.assertEqual(response.status_code, 200)

    def test_order_history_view_uses_correct_template_with_orders(self):
        self.client.login(username="testuser", password="testpass123")

        models.Order.objects.create(
            user=user_models.User.objects.get(username="testuser"),
            address1="address1",
            address2="address2",
            address3="address3",
            town="town",
            postcode="postcode",
            phone="phone",
            justification="test",
            status="wait",
            comments="comments",
        )

        response = self.client.get(reverse("cyod:order_history"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_history.html")
        models.Order.objects.all().delete()

    def test_order_history_view_uses_correct_context(self):
        self.client.login(username="testuser", password="testpass123")
        models.Order.objects.create(
            user=user_models.User.objects.get(username="testuser"),
        )
        response = self.client.get(reverse("cyod:order_history"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("orders", response.context)
        models.Order.objects.all().delete()

    def test_order_history_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("cyod:order_history"))
        self.assertRedirects(response, "/user/login/")


class BasketViewTest(testcases.TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user()

        models.Product.objects.create(
            name="iphone",
            product_type="pho",
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"mock image", content_type="image/jpeg"
            ),
            release=datetime.now(),
            description="test",
            roles_allowed="all",
        )

        models.OrderItem.objects.create(
            product=models.Product.objects.get(name="iphone"),
            quantity=1,
            order=models.Order.objects.create(
                user=user_models.User.objects.get(username="testuser"),
            ),
            order_type="req",
        )

    @classmethod
    def tearDownClass(cls):
        product = models.Product.objects.get(name="iphone")
        os.remove(os.path.join(settings.MEDIA_ROOT, product.image.name))
        super().tearDownClass()

    def test_basket_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/choose-your-own-device/basket/")
        self.assertEqual(response.status_code, 200)

    def test_basket_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:basket"))
        self.assertEqual(response.status_code, 200)

    def test_basket_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:basket"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/basket.html")

    def test_basket_view_uses_correct_context(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:basket"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("formset", response.context)

    def test_basket_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("cyod:basket"))
        self.assertRedirects(response, "/user/login/")


class OrderViewTest(testcases.TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user()

        models.Product.objects.create(
            name="iphone",
            product_type="pho",
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"mock image", content_type="image/jpeg"
            ),
            release=datetime.now(),
            description="test",
            roles_allowed="all",
        )

        models.OrderItem.objects.create(
            product=models.Product.objects.get(name="iphone"),
            quantity=1,
            order=models.Order.objects.create(
                user=user_models.User.objects.get(username="testuser"),
            ),
            order_type="req",
        )

    @classmethod
    def tearDownClass(cls):
        product = models.Product.objects.get(name="iphone")
        os.remove(os.path.join(settings.MEDIA_ROOT, product.image.name))
        super().tearDownClass()

    def test_order_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/choose-your-own-device/order/")
        self.assertEqual(response.status_code, 200)

    def test_order_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:order"))
        self.assertEqual(response.status_code, 200)

    def test_order_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:order"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order.html")

    def test_order_view_uses_correct_context(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:order"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_order_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("cyod:order"))
        self.assertRedirects(response, "/user/login/")

    def test_order_view_redirects_to_basket_if_no_items_in_basket(self):
        self.client.login(username="testuser", password="testpass123")
        models.OrderItem.objects.all().delete()
        response = self.client.get(reverse("cyod:order"))
        self.assertEqual(response.status_code, 302)
        models.OrderItem.objects.create(
            product=models.Product.objects.get(name="iphone"),
            quantity=1,
            order=models.Order.objects.create(
                user=user_models.User.objects.get(username="testuser"),
            ),
            order_type="req",
        )


class OrderConfirmationViewTest(testcases.TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user()

    def test_order_confirmation_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/choose-your-own-device/order/confirmed")
        self.assertEqual(response.status_code, 200)

    def test_order_confirmation_view_url_accessible_by_name(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:order_done"))
        self.assertEqual(response.status_code, 200)

    def test_order_confirmation_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("cyod:order_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/confirmation.html")

    def test_order_confirmation_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse("cyod:order_done"))
        self.assertEqual(response.status_code, 302)
