from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("inscription/", views.register, name="register"),
    path("connexion/", views.login_view, name="login"),
    path("deconnexion/", views.logout_view, name="logout"),
    path("mon-compte/", views.account_home, name="account_home"),
    path("mes-commandes/", views.order_list, name="order_list"),
    path("mes-commandes/<int:order_id>/", views.order_detail, name="order_detail"),
    path("mes-devis/", views.quote_list, name="quote_list"),
    path("mes-devis/<int:quote_id>/", views.quote_detail, name="quote_detail"),
]
