# orders/models.py

from django.db import models
from django.contrib.auth.models import User

# 店舗マスター
class Store(models.Model):
    name = models.CharField("店舗名", max_length=100)
    def __str__(self): return self.name

# ジャンルマスター
class Genre(models.Model):
    name = models.CharField("ジャンル名", max_length=100)
    def __str__(self): return self.name

# 【新規】商品データ（あなたが登録するリスト）
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="顧客")
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, verbose_name="店舗")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name="ジャンル")
    
    name = models.CharField("商品名", max_length=200)
    spec = models.TextField("基本仕様", blank=True)
    price = models.IntegerField("単価", default=0)
    image = models.ImageField("商品写真", upload_to='products/', blank=True, null=True)
    
    created_at = models.DateTimeField("登録日", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

# 注文履歴データ
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="顧客")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="商品")
    
    order_date = models.DateTimeField("注文日時", auto_now_add=True)
    delivery_date = models.DateField("希望納品日", null=True, blank=True)
    
    quantity = models.IntegerField("数量", default=1)
    orderer_name = models.CharField("依頼者名", max_length=100)
    has_changes = models.BooleanField("変更点の有無", default=False)
    note = models.TextField("備考・変更点", blank=True)
    
    price_at_order = models.IntegerField("注文時価格", default=0)

    def __str__(self):
        return f"{self.order_date} - {self.product.name}"