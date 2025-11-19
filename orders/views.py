# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Order, Store, Genre
from .forms import OrderForm

# ログイン
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})

# ログアウト
def custom_logout(request):
    logout(request)
    return redirect('login')

# ① 商品一覧（検索機能付き）
@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user).order_by('-created_at')
    
    # 店舗で絞り込み
    store_id = request.GET.get('store')
    if store_id:
        products = products.filter(store_id=store_id)

    # ジャンルで絞り込み（機能追加）
    genre_id = request.GET.get('genre')
    if genre_id:
        products = products.filter(genre_id=genre_id)

    context = {
        'products': products,
        'stores': Store.objects.all(),
        'genres': Genre.objects.all(), # ジャンル一覧も画面に渡す
    }
    return render(request, 'orders/product_list.html', context)

# ② 注文入力・確認・送信機能
@login_required
def create_order(request, product_id):
    target_product = get_object_or_404(Product, id=product_id, user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if 'confirm' in request.POST:
            if form.is_valid():
                return render(request, 'orders/order_confirm.html', {
                    'form': form,
                    'product': target_product
                })

        elif 'send' in request.POST:
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.user = request.user
                new_order.product = target_product
                new_order.price_at_order = 0 
                new_order.save()

                subject = f"【見積・発注依頼】{target_product.name}"
                message = f"""
商品名: {target_product.name}
依頼者: {new_order.orderer_name}
数量: {new_order.quantity}
納期: {new_order.delivery_date}
変更: {'あり' if new_order.has_changes else 'なし'}
備考:
{new_order.note}

※数量・納期を確認の上、担当者へ見積を送ってください。
"""
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                except:
                    print("メール送信エラー")

                return redirect('order_history')

    else:
        form = OrderForm()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'product': target_product
    })

# ③ 注文履歴一覧
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/order_history.html', {'orders': orders})