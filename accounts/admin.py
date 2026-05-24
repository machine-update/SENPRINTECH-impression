from django.contrib import admin

from .models import EmailVerificationCode


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "attempts", "resend_count", "verified_at", "created_at")
    list_filter = ("verified_at", "created_at", "expires_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = (
        "user",
        "code_hash",
        "attempts",
        "resend_count",
        "expires_at",
        "last_sent_at",
        "verified_at",
        "created_at",
        "updated_at",
    )
