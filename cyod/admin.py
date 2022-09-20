from django.contrib import admin

from cyod.models import Product, Order, OrderItem

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [ 
        ( 'Address & Contact Information', 
            {
                'fields':
                [
                    'address1',
                    'address2',
                    'address3',
                    'postcode',
                    'phone',

                ]
            }
        ),
        ('Order Information1994 ',
            {
                'fields':
                [
                    'justification',
                    'status',
                    'comments',
                    'date_placed',
                ]
            }
        )
    ]
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(Order,OrderAdmin)


