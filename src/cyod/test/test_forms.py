from typing_extensions import assert_type
from django.test import testcases

from cyod import forms

class OrderItemProductViewForm(testcases.TestCase):
    def setup_orderitem_form(self):
        form = forms.OrderItemProductViewForm(data={'quantity':1, 'order_type':'ret'})
        return form

    def test_order_type_initial(self):
        form = self.setup_orderitem_form()
        self.assertEqual(len(form.base_fields.get('order_type').choices), 2)

    def test_quantity_initial(self):
        form = self.setup_orderitem_form()
        self.assertEqual(form.base_fields.get('quantity').initial, 1)
    
    def test_quantity_min_value(self):
        form = self.setup_orderitem_form()
        self.assertEqual(form.base_fields.get('quantity').min_value, 1)
    
    def test_quantity_max_value(self):
        form = self.setup_orderitem_form()
        self.assertEqual(form.base_fields.get('quantity').max_value, 99)
    

class BasketFormTest(testcases.TestCase):
        def setup_order_form(self):
            form = forms.BasketForm(data={'product_name':'test', 'quantity':1, 'order_type':'ret'})
            return form
        
        def test_product_name_disabled(self):
            form = self.setup_order_form()
            self.assertEqual(form.base_fields.get('product_name').disabled, True)
        
        def test_quantity_min_value(self):
            form = self.setup_order_form()
            self.assertEqual(form.base_fields.get('quantity').min_value, 1)
        
        def test_quantity_max_value(self):
            form = self.setup_order_form()
            self.assertEqual(form.base_fields.get('quantity').max_value, 99)
        
        def test_order_type_initial(self):
            form = self.setup_order_form()
            self.assertEqual(len(form.base_fields.get('order_type').choices), 2)


class OrderFormTest(testcases.TestCase):
    def setup_order_form(self,postcode='ln13 0ns',phone='01234567890'):
        form = forms.OrderForm(data={
            'address1':'test',
            'address2':'test',
            'address3':'test',
            'town':'test',
            'postcode':postcode,
            'phone':phone,
            'justification':'test',
            })
        return form

    def test_address1_required(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address1').required, True)

    def test_address1_label(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address1').label, 'Address 1')

    def test_address2_required(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address2').required, False)

    def test_address3_label(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address2').label, 'Address 2')

    def test_address2_help_text(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address2').help_text, 'Not required')
    
    def test_address3_required(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address3').required, False)

    def test_address3_label(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address3').label, 'Address 3')
    
    def test_address3_help_text(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('address3').help_text, 'Not required')

    def test_town_required(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('town').required, True)

    def test_town_label(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('town').label, 'Town')
    
    def test_postcode_required(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('postcode').required, True)

    def test_postcode_postcode_validator_returns_error(self):
        form = self.setup_order_form(postcode='bad')
        self.assertEqual(form.errors["postcode"], ['Please enter a valid postcode'])

    def test_postcode_postcode_validator_accepts_good_postcodes(self):
        form = self.setup_order_form()
        self.assertNotIn('postcode',form.errors)
    
    def test_phone_required(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('phone').required, True)

    def test_phone_validator_returns_error(self):
        form = self.setup_order_form(phone='bad')
        self.assertEqual(form.errors["phone"], ['Please enter a valid phonenumber'])

    def test_phone_validator_accepts_good_phone_numbers(self):
        form = self.setup_order_form()
        self.assertNotIn('phone',form.errors)
    
    def test_justification_required(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('justification').required, False)

    def test_justification_help_text(self):
        form = self.setup_order_form()
        self.assertEqual(form.base_fields.get('justification').help_text, 'Max 500 chars. Not required')


