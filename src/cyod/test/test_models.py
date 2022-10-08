from datetime import datetime

from django.test import TestCase

from cyod import models
from user import models as user_models

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.Product.objects.create(
        name='name',
        product_type='lap',
        release=datetime.now(),
        description='test',
        roles_allowed='all')

    def test_name_label(self):
        product = models.Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
    
    def test_name_max_length(self):
        product = models.Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_product_type_label(self):
        product = models.Product.objects.get(id=1)
        field_label = product._meta.get_field('product_type').verbose_name
        self.assertEquals(field_label, 'product type')

    def test_product_type_max_length(self):
        product = models.Product.objects.get(id=1)
        max_length = product._meta.get_field('product_type').max_length
        self.assertEquals(max_length, 3)

    def test_release_label(self):
        product = models.Product.objects.get(id=1)
        field_label = product._meta.get_field('release').verbose_name
        self.assertEquals(field_label, 'release')
    
    def test_description_label(self):
        product = models.Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')
    
    def test_description_max_length(self):
        product = models.Product.objects.get(id=1)
        max_length = product._meta.get_field('description').max_length
        self.assertEquals(max_length, 500)

    def test_roles_allowed_label(self):
        product = models.Product.objects.get(id=1)
        field_label = product._meta.get_field('roles_allowed').verbose_name
        self.assertEquals(field_label, 'roles allowed')

    def test_roles_allowed_max_length(self):
        product = models.Product.objects.get(id=1)
        max_length = product._meta.get_field('roles_allowed').max_length
        self.assertEquals(max_length, 5)
    
    def test_object_name_is_name(self):
        product = models.Product.objects.get(id=1)
        expected_object_name = f'{product.name}'
        self.assertEquals(expected_object_name, str(product))
    
class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = user_models.User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='test',
            last_name='user',
        )

        models.Order.objects.create(
        user = user,
        address1='address1',
        address2='address2',
        address3='address3',
        town='town',
        postcode='postcode',
        phone='phone',
        justification='test',
        status='wait',
        comments='comments')

    def test_address1_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('address1').verbose_name
        self.assertEquals(field_label, 'address1')
    
    def test_address1_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('address1').max_length
        self.assertEquals(max_length, 50)

    def test_address2_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('address2').verbose_name
        self.assertEquals(field_label, 'address2')
    
    def test_address2_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('address2').max_length
        self.assertEquals(max_length, 50)

    def test_address3_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('address3').verbose_name
        self.assertEquals(field_label, 'address3')
    
    def test_address3_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('address3').max_length
        self.assertEquals(max_length, 50)

    def test_town_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('town').verbose_name
        self.assertEquals(field_label, 'town')
    
    def test_town_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('town').max_length
        self.assertEquals(max_length, 50)

    def test_postcode_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('postcode').verbose_name
        self.assertEquals(field_label, 'postcode')
    
    def test_postcode_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta

    def test_phone_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'phone')
    
    def test_phone_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('phone').max_length
        self.assertEquals(max_length, 13)
    
    def test_justification_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('justification').verbose_name
        self.assertEquals(field_label, 'justification')

    def test_justification_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('justification').max_length
        self.assertEquals(max_length, 500)

    def test_status_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_status_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('status').max_length
        self.assertEquals(max_length, 5)

    def test_comments_label(self):
        order = models.Order.objects.get(id=1)
        field_label = order._meta.get_field('comments').verbose_name
        self.assertEquals(field_label, 'comments')

    def test_comments_max_length(self):
        order = models.Order.objects.get(id=1)
        max_length = order._meta.get_field('comments').max_length
        self.assertEquals(max_length, 500)

    def test_object_name_is_id(self):
        order = models.Order.objects.get(id=1)
        expected_object_name = f'{order.id}'
        self.assertEquals(expected_object_name, str(order))

    def test_date_placed_is_none(self):
        order = models.Order.objects.get(id=1)
        self.assertIsNone(order.date_placed)

class  OrderItem(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = models.Product.objects.create(
        name='name',
        product_type='lap',
        release=datetime.now(),
        description='test',
        roles_allowed='all')

        user = user_models.User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='test',
            last_name='user',
        )

        order = models.Order.objects.create(
        user = user,
        address1='address1',
        address2='address2',
        address3='address3',
        town='town',
        postcode='postcode',
        phone='phone',
        justification='test',
        status='wait',
        comments='comments')

        models.OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        order_type = 'ret')

    def test_order_label(self):
        orderitem = models.OrderItem.objects.get(id=1)
        field_label = orderitem._meta.get_field('order').verbose_name
        self.assertEquals(field_label, 'order')
    
    def test_product_label(self):
        orderitem = models.OrderItem.objects.get(id=1)
        field_label = orderitem._meta.get_field('product').verbose_name
        self.assertEquals(field_label, 'product')
    
    def test_quantity_label(self):
        orderitem = models.OrderItem.objects.get(id=1)
        field_label = orderitem._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')
    
    def test_order_type_label(self):
        orderitem = models.OrderItem.objects.get(id=1)
        field_label = orderitem._meta.get_field('order_type').verbose_name
        self.assertEquals(field_label, 'order type')
    
    def test_order_type_max_length(self):
        orderitem = models.OrderItem.objects.get(id=1)
        max_length = orderitem._meta.get_field('order_type').max_length
        self.assertEquals(max_length, 4)
    
