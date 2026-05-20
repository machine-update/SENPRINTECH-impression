from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from urllib.parse import quote
from cart.models import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order


def build_order_whatsapp_url(order):
    lines = [
        f"Bonjour SenPrinTech, voici ma commande #{order.id}.",
        f"Client: {order.full_name}",
        f"Telephone: {order.phone or '-'}",
        f"Email: {order.email}",
        f"Livraison: {order.get_delivery_method_display()}",
        f"Adresse: {order.address}, {order.city}".strip().strip(","),
        "Produits:",
    ]
    for item in order.items.select_related("product").all():
        lines.append(f"- {item.product.name} x{item.quantity}: {item.get_cost()} FCFA")
    lines.extend([
        f"Total: {order.get_total_cost()} FCFA",
        f"Paiement: {order.get_payment_status_display()}",
    ])
    if order.notes:
        lines.append(f"Notes: {order.notes}")
    message = "\n".join(lines)
    return f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(message)}"


@login_required(login_url="accounts:login")
def order_create(request):
    cart=None
    cart_id = request.session.get('cart_id')
    
    if not cart_id:
        return redirect("cart:cart_detail")

    cart = get_object_or_404(Cart, id=cart_id)
    if not cart.items.exists():
        return redirect("cart:cart_detail")
    
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    price = item.configured_price or item.product.price,
                    quantity = item.quantity,
                    selected_options = item.selected_options,
                    uploaded_file = item.uploaded_file,
                )
            cart.delete()
            del request.session["cart_id"]
            return redirect("orders:order_confirmation", order.id)

    else:
        initial = {
            "full_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }
        form = OrderCreateForm(initial=initial)

    return render(request, "orders/order_create.html", {
        "cart":cart, "form":form
    })

@login_required(login_url="accounts:login")
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_confirmation.html", {
        "order": order,
        "whatsapp_order_url": build_order_whatsapp_url(order),
    })
