from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import quote

from .forms import ContactForm, ProductConfigurationForm
from .models import Category, Product


def get_catalog_context(category_slug=None, contact_form=None):
    category = None
    categories = Category.objects.all().order_by("name")
    products = Product.objects.filter(available=True).select_related("category").order_by("-created")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return {
        "category": category,
        "products": products,
        "categories": categories,
        "contact_form": contact_form or ContactForm(),
    }


def product_list(request, category_slug=None):
    return render(request, 'products/product/list.html', get_catalog_context(category_slug))


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("options__choices"),
        id=id,
        slug=slug,
        available=True,
    )
    configuration_form = ProductConfigurationForm(product=product)
    whatsapp_message = (
        f"Bonjour SenPrinTech, je suis interesse par ce produit : {product.name}. "
        "Pouvez-vous me conseiller ?"
    )
    return render(
        request,
        'products/product/detail.html',
        {
            'product': product,
            "configuration_form": configuration_form,
            "product_whatsapp_url": f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(whatsapp_message)}",
        },
    )


def contact_submit(request):
    if request.method != "POST":
        return redirect("products:product_list")

    form = ContactForm(request.POST)
    if form.is_valid():
        messages.success(
            request,
            "Votre demande a bien ete envoyee. L'equipe SenPrinTech vous recontacte rapidement.",
        )
        return redirect("products:product_list")

    messages.error(request, "Veuillez corriger les champs du formulaire de contact.")
    return render(request, "products/product/list.html", get_catalog_context(contact_form=form))
