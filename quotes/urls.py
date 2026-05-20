from django.urls import path

from . import views


app_name = "quotes"

urlpatterns = [
    path("entreprise/", views.enterprise_quote, name="enterprise_quote"),
]
