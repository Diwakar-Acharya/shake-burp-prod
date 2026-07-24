from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.accounts.views import (
    login_view,
    register_view,
    logout_view,
    profile_view,
    change_password_view,
)
from apps.payments.views import (
    initiate_checkout_view,
    payment_success_view,
    payment_cancel_view,
    stripe_webhook_view,
)
from apps.products.models import Product

# ── Secret Admin URL Key ──────────────────────────────────────────────────────
# Admin is only accessible at /manage-sb-x9k2/
# The standard /admin/ path is intentionally disabled.
ADMIN_SECRET_PATH = "manage-sb-x9k2"

# ── Views ──────────────────────────────────────────────────────────────────────

def home_view(request):
    products = Product.objects.filter(is_active=True).order_by('id')[:3]
    return render(request, "pages/home.html", {"page": "home", "products": products})


def catalog_view(request):
    products = Product.objects.filter(is_active=True).order_by('id')
    return render(request, "pages/catalog.html", {"page": "catalog", "products": products})


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "pages/product_detail.html", {"page": "catalog", "product": product})


def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = []
    subtotal = 0
    for slug, qty in cart.items():
        try:
            p_obj = Product.objects.get(slug=slug, is_active=True)
            p = {
                "slug": p_obj.slug,
                "name": p_obj.name,
                "price": p_obj.price,
                "badge": p_obj.badge,
                "badge_class": p_obj.badge_class,
                "desc": p_obj.desc,
                "specs": p_obj.specs,
                "color": p_obj.color,
                "svg": p_obj.svg,
                "qty": qty,
                "total": p_obj.price * qty,
            }
            subtotal += p["total"]
            cart_items.append(p)
        except Product.DoesNotExist:
            continue
    return render(request, "pages/cart.html", {
        "page": "cart",
        "cart_items": cart_items,
        "subtotal": subtotal,
        "cart_count": sum(cart.values()),
    })


@require_POST
def add_to_cart_view(request):
    slug = request.POST.get("slug")
    try:
        qty = max(1, int(request.POST.get("qty", 1)))
    except (ValueError, TypeError):
        qty = 1
    if Product.objects.filter(slug=slug, is_active=True).exists():
        cart = request.session.get("cart", {})
        cart[slug] = cart.get(slug, 0) + qty
        request.session["cart"] = cart
    return redirect("cart")


@require_POST
def create_order_and_checkout_view(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart")

    total_amount = 0
    items_to_create = []

    for slug, qty in cart.items():
        try:
            p_obj = Product.objects.get(slug=slug, is_active=True)
            line_total = p_obj.price * qty
            total_amount += line_total
            items_to_create.append((p_obj, qty, p_obj.price))
        except Product.DoesNotExist:
            continue

    if not items_to_create:
        return redirect("cart")

    from apps.orders.models import Order, OrderItem
    user = request.user if request.user.is_authenticated else None
    email = user.email if (user and user.email) else "customer@shakeandburp.com"
    first_name = user.first_name if (user and user.first_name) else (user.username if user else "Guest")
    last_name = user.last_name if (user and user.last_name) else "Customer"

    order = Order.objects.create(
        user=user,
        email=email,
        first_name=first_name,
        last_name=last_name,
        address="123 Main Street",
        city="Mumbai",
        postal_code="400001",
        country="India",
        total_amount=total_amount,
        status="pending"
    )

    for p_obj, qty, price in items_to_create:
        OrderItem.objects.create(
            order=order,
            product=p_obj,
            product_name=p_obj.name,
            price=price,
            quantity=qty
        )

    # Clear session cart
    request.session["cart"] = {}

    return redirect("initiate_checkout", order_id=order.id)


@require_POST
def remove_from_cart_view(request, slug):
    cart = request.session.get("cart", {})
    if slug in cart:
        del cart[slug]
        request.session["cart"] = cart
    return redirect("cart")


@require_POST
def clear_cart_view(request):
    request.session["cart"] = {}
    return redirect("cart")


@require_POST
def update_cart_qty_view(request, slug):
    try:
        qty = int(request.POST.get("qty", 1))
    except (ValueError, TypeError):
        qty = 1
    cart = request.session.get("cart", {})
    if Product.objects.filter(slug=slug, is_active=True).exists():
        if qty > 0:
            cart[slug] = qty
        else:
            cart.pop(slug, None)
        request.session["cart"] = cart
    return redirect("cart")


def contact_view(request):
    return render(request, "pages/contact.html", {"page": "contact"})


def privacy_view(request):
    return render(request, "pages/privacy.html", {"page": "privacy"})


def terms_view(request):
    return render(request, "pages/terms.html", {"page": "terms"})


# ── URL Patterns ───────────────────────────────────────────────────────────────

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{ADMIN_SECRET_PATH}/", admin.site.urls),

    # Pages
    path("", home_view, name="home"),
    path("catalog/", catalog_view, name="catalog"),
    path("shaker/<slug:slug>/", product_detail_view, name="product_detail"),
    path("cart/", cart_view, name="cart"),
    path("contact/", contact_view, name="contact"),
    path("privacy/", privacy_view, name="privacy"),
    path("terms/", terms_view, name="terms"),

    # Cart actions (all POST-only for CSRF safety)
    path("cart/add/", add_to_cart_view, name="add_to_cart"),
    path("cart/remove/<slug:slug>/", remove_from_cart_view, name="remove_from_cart"),
    path("cart/clear/", clear_cart_view, name="clear_cart"),
    path("cart/update/<slug:slug>/", update_cart_qty_view, name="update_cart_qty"),

    # Auth & OAuth
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/password/", change_password_view, name="change_password"),
    path("accounts/", include("allauth.urls")),

    # Stripe Payments & Webhooks
    path("checkout/create/", create_order_and_checkout_view, name="create_order_and_checkout"),
    path("checkout/stripe/<int:order_id>/", initiate_checkout_view, name="initiate_checkout"),
    path("checkout/success/", payment_success_view, name="payment_success"),
    path("checkout/cancel/", payment_cancel_view, name="payment_cancel"),
    path("payments/webhook/stripe/", stripe_webhook_view, name="stripe_webhook"),
]


def error_404_view(request, exception=None):
    return render(request, "404.html", {"page": "error"}, status=404)


def error_403_view(request, exception=None):
    return render(request, "403.html", {"page": "error"}, status=403)


def error_500_view(request):
    return render(request, "500.html", {"page": "error"}, status=500)


handler404 = error_404_view
handler403 = error_403_view
handler500 = error_500_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
