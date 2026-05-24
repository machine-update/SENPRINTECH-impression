from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views


app_name = "accounts"

urlpatterns = [
    path("inscription/", views.register, name="register"),
    path("connexion/", views.login_view, name="login"),
    path("deconnexion/", views.logout_view, name="logout"),
    path("verification-email/", views.verify_email, name="verify_email"),
    path("renvoyer-code/", views.resend_verification_code, name="resend_verification"),
    path(
        "mot-de-passe-oublie/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/emails/password_reset_email.txt",
            html_email_template_name="accounts/emails/password_reset_email.html",
            subject_template_name="accounts/emails/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "mot-de-passe-oublie/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("mon-compte/", views.account_home, name="account_home"),
    path("mes-commandes/", views.order_list, name="order_list"),
    path("mes-commandes/<int:order_id>/", views.order_detail, name="order_detail"),
    path("mes-devis/", views.quote_list, name="quote_list"),
    path("mes-devis/<int:quote_id>/", views.quote_detail, name="quote_detail"),
]
