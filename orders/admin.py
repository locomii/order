# orders/admin.py

from django.contrib import admin
from .models import Store, Genre, Product, Order

class ProductAdmin(admin.ModelAdmin):
    # 価格(price)を一覧から削除しました
    list_display = ('name', 'user', 'store', 'created_at')
    list_filter = ('user', 'store')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'user', 'product', 'quantity', 'orderer_name')
    list_filter = ('user', 'order_date')

admin.site.register(Store)
admin.site.register(Genre)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)