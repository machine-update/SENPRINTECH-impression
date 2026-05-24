from django.shortcuts import render


LEGAL_PAGES = {
    "privacy": "legal/privacy.html",
    "terms": "legal/terms.html",
    "sales": "legal/sales.html",
    "delivery": "legal/delivery.html",
    "returns": "legal/returns.html",
    "legal_notice": "legal/legal_notice.html",
    "faq": "legal/faq.html",
}


def legal_page(request, page):
    return render(request, LEGAL_PAGES[page])
