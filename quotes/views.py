from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import QuoteRequestForm
from .models import QuoteRequest


def enterprise_quote(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            if request.user.is_authenticated:
                quote.user = request.user
            quote.save()
            messages.success(request, "Votre demande de devis a bien ete envoyee.")
            return redirect("quotes:enterprise_quote")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "contact_name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        form = QuoteRequestForm(initial=initial)

    return render(request, "quotes/enterprise_quote.html", {"form": form})


@login_required(login_url="accounts:login")
def my_quotes(request):
    quotes = request.user.quote_requests.all()
    return render(request, "quotes/my_quotes.html", {"quotes": quotes})


@login_required(login_url="accounts:login")
def quote_detail(request, quote_id):
    quote = get_object_or_404(QuoteRequest, id=quote_id, user=request.user)
    return render(request, "quotes/quote_detail.html", {"quote": quote})
