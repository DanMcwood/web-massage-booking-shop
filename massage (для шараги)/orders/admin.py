from django.contrib import admin
from import_export import resources, fields, formats
from import_export.admin import ExportMixin
from .models import Order, OrderItem
from django.http import HttpResponse
import csv

class UTF8CSV(formats.base_formats.CSV):
    def export_data(self, dataset, **kwargs):
        csv_data = super().export_data(dataset, **kwargs)
        bom = b'\xef\xbb\xbf'
        return bom + csv_data

class OrderResource(resources.ModelResource):
    product_name = fields.Field(column_name='product_name')
    product_quantity = fields.Field(column_name='product_quantity')
    product_price = fields.Field(column_name='product_price')

    class Meta:
        model = Order
        fields = ('id', 'full_name', 'email', 'city', 'paid', 'payment_method', 'created_at')
        export_order = fields
        formats = [UTF8CSV]

    def dehydrate_product_name(self, order):
        items = order.items.all()
        return ', '.join(item.product.name for item in items) if items.exists() else ''

    def dehydrate_product_quantity(self, order):
        items = order.items.all()
        return ', '.join(str(item.quantity) for item in items) if items.exists() else ''

    def dehydrate_product_price(self, order):
        items = order.items.all()
        return ', '.join(str(item.price) for item in items) if items.exists() else ''


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_description', 'price', 'quantity')
    can_delete = False
    show_change_link = True

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Название'

    def product_description(self, obj):
        return obj.product.description
    product_description.short_description = 'Описание'

    def price(self, obj):
        return obj.price
    price.short_description = 'Цена'

    def quantity(self, obj):
        return obj.quantity
    quantity.short_description = 'Количество'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportMixin):
    list_display = ('id', 'full_name', 'email', 'city', 'paid', 'payment_method', 'created_at')
    list_filter = ('paid', 'payment_method', 'created_at')
    search_fields = ('full_name', 'email', 'address', 'city')
    inlines = [OrderItemInline]

    actions = ['export_orders_with_items']

    def export_orders_with_items(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="orders_with_items.csv"'
        response.write('\ufeff'.encode('utf-8'))

        writer = csv.writer(response)
        writer.writerow([
            'Order ID', 'Full Name', 'Email', 'City', 'Paid', 'Payment Method', 'Created At',
            'Product Name', 'Product Description', 'Price', 'Quantity'
        ])

        for order in queryset:
            items = order.items.all()
            if items.exists():
                for item in items:
                    writer.writerow([
                        order.id, order.full_name, order.email, order.city,
                        order.paid, order.payment_method, order.created_at,
                        item.product.name, item.product.description, item.price, item.quantity
                    ])
            else:
                writer.writerow([
                    order.id, order.full_name, order.email, order.city,
                    order.paid, order.payment_method, order.created_at,
                    '', '', '', ''
                ])

        return response

    export_orders_with_items.short_description = "Экспорт заказов с товарами (CSV)"
