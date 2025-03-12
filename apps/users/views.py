from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserUpdateForm
from .forms import UserRegistrationForm
from django.contrib.auth import update_session_auth_hash, logout
from apps.products.models import Product
from apps.cart.models import CartItem


# 如果你没有收藏功能，可以暂时不传 favorites
# from apps.reviews.models import Favorite


# 用户注册
def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # 确保密码加密
            user.save()
            login(request, user)  # 自动登录
            return redirect('profile')  # 跳转到 profile 页面
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# 账户设置（集成修改密码 & 个人资料）
def account_settings(request):
    if not request.user.is_authenticated:
        # 用户未登录时，显示提示页面，并传入 next 参数
        return render(request, 'need_login.html', {'next': '/account-settings/'})

    if request.method == "POST":
        profile_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if "update_profile" in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect('account_settings')

        if "change_password" in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('account_settings')
    else:
        profile_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, "account_settings.html", {
        "profile_form": profile_form,
        "password_form": password_form
    })

# 用户注销
def user_logout(request):
    logout(request)
    return redirect('/login/')  # 退出后跳转到登录页面


@login_required
def user_profile(request):
    user = request.user
    user_products = Product.objects.filter(seller=user)
    print("User Products Count:", user_products.count())  # 通过终端输出调试信息
    my_cart = CartItem.objects.filter(user=user)
    return render(request, "profile.html", {
        "user": user,
        "user_products": user_products,
        "my_cart": my_cart,
    })

