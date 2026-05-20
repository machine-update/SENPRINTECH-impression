from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order
from quotes.models import QuoteRequest

from .forms import CustomerLoginForm, CustomerRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:account_home")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte SenPrinTech a ete cree.")
            return redirect(request.GET.get("next") or "accounts:account_home")
    else:
        form = CustomerRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:account_home")

    if request.method == "POST":
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Connexion reussie.")
            return redirect(request.GET.get("next") or "accounts:account_home")
    else:
        form = CustomerLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Vous etes deconnecte.")
    return redirect("products:product_list")


@login_required(login_url="accounts:login")
def account_home(request):
    recent_orders = request.user.orders.prefetch_related("items__product").order_by("-created_at")[:3]
    recent_quotes = request.user.quote_requests.order_by("-created_at")[:3]
    return render(
        request,
        "accounts/account_home.html",
        {"recent_orders": recent_orders, "recent_quotes": recent_quotes},
    )


@login_required(login_url="accounts:login")
def order_list(request):
    orders = request.user.orders.prefetch_related("items__product").order_by("-created_at")
    return render(request, "accounts/order_list.html", {"orders": orders})


@login_required(login_url="accounts:login")
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user,
    )
    return render(request, "accounts/order_detail.html", {"order": order})


@login_required(login_url="accounts:login")
def quote_list(request):
    quotes = request.user.quote_requests.order_by("-created_at")
    return render(request, "quotes/my_quotes.html", {"quotes": quotes})


@login_required(login_url="accounts:login")
def quote_detail(request, quote_id):
    quote = get_object_or_404(QuoteRequest, id=quote_id, user=request.user)
    return render(request, "quotes/quote_detail.html", {"quote": quote})
