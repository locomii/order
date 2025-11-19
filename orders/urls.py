# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # 商品リスト（ここがトップページになります）
    path('', views.product_list, name='product_list'),
    
    # 注文画面
    path('order/<int:product_id>/', views.create_order, name='create_order'),
    
    # 注文履歴
    path('history/', views.order_history, name='order_history'),
]