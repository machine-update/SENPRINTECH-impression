from django.contrib import admin
from django.utils.html import format_html, format_html_join

from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]
    readonly_fields = ["selected_options_display", "uploaded_file_link"]
    fields = [
        "product",
        "price",
        "quantity",
        "selected_options_display",
        "uploaded_file_link",
    ]

    def selected_options_display(self, obj):
        if not obj or not obj.selected_options:
            return "-"

        items = format_html_join(
            "",
            "<li><strong>{}:</strong> {}</li>",
            (
                (option.get("name", ""), option.get("label") or option.get("value", ""))
                for option in obj.selected_options
            ),
        )
        return format_html("<ul style='margin:0; padding-left:18px'>{}</ul>", items)

    selected_options_display.short_description = "Options choisies"

    def uploaded_file_link(self, obj):
        if not obj or not obj.uploaded_file:
            return "Aucun fichier fourni"
        return format_html(
            "<a href='{}' target='_blank' rel='noopener'>{}</a>",
            obj.uploaded_file.url,
            obj.uploaded_file.name.split("/")[-1],
        )

    uploaded_file_link.short_description = "Fichier client"


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    can_delete = False
    readonly_fields = ["previous_status", "new_status", "note", "created_at"]
    fields = ["previous_status", "new_status", "note", "created_at"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "id",
        "full_name",
        "phone",
        "email",
        "status_badge",
        "priority_badge",
        "deadline_badge",
        "assigned_to",
        "delivery_method",
        "payment_method",
        "payment_status",
        "payment_badge",
        "total_display",
        "created_at",
    ]
    list_filter = [
        "status",
        "priority",
        "assigned_to",
        "delivery_method",
        "payment_method",
        "payment_status",
        "production_deadline",
        "created_at",
    ]
    list_editable = ["assigned_to", "payment_status"]
    search_fields = [
        "id",
        "order_number",
        "full_name",
        "phone",
        "email",
        "address",
        "city",
        "user__username",
        "payment_method",
        "payment_reference",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    actions = [
        "mark_payment_pending",
        "mark_payment_paid",
        "mark_payment_failed",
        "mark_payment_refunded",
    ]
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    readonly_fields = (
        "created_at",
        "updated_at",
        "total_display",
        "proof_file_link",
        "order_number",
        "paid",
    )
    fieldsets = [
        ("Client", {"fields": ["order_number", "user", "full_name", "phone", "email", "address", "city", "delivery_method", "notes"]}),
        ("Production", {"fields": ["status", "priority", "production_deadline", "assigned_to", "internal_notes"]}),
        ("BAT / apercu", {"fields": ["proof_file", "proof_file_link"]}),
        ("Paiement", {"fields": ["payment_method", "payment_status", "payment_provider", "payment_reference", "paid"]}),
        ("Resume", {"fields": ["total_display", "created_at", "updated_at"]}),
    ]

    @admin.display(description="Statut", ordering="status")
    def status_badge(self, obj):
        colors = {
            Order.PENDING: "#6b7280",
            Order.FILE_RECEIVED: "#2563eb",
            Order.REVIEWING: "#7c3aed",
            Order.CLIENT_VALIDATION: "#b45309",
            Order.PRINTING: "#111827",
            Order.FINISHING: "#374151",
            Order.PACKAGING: "#4b5563",
            Order.SHIPPED: "#0f766e",
            Order.DELIVERED: "#15803d",
            Order.CANCELLED: "#b91c1c",
        }
        return format_html(
            "<span class='sp-admin-badge' style='--badge-color:{}'>{}</span>",
            colors.get(obj.status, "#6b7280"),
            obj.get_status_display(),
        )

    @admin.display(description="Priorite", ordering="priority")
    def priority_badge(self, obj):
        color = "#b91c1c" if obj.priority == Order.PRIORITY_URGENT else "#4b5563"
        return format_html(
            "<span class='sp-admin-badge' style='--badge-color:{}'>{}</span>",
            color,
            obj.get_priority_display(),
        )

    @admin.display(description="Deadline", ordering="production_deadline")
    def deadline_badge(self, obj):
        if not obj.production_deadline:
            return "-"
        return format_html("<strong>{}</strong>", obj.production_deadline.strftime("%d/%m/%Y"))

    @admin.display(description="Paiement", ordering="payment_status")
    def payment_badge(self, obj):
        colors = {
            Order.PAYMENT_PENDING: "#b45309",
            Order.PAYMENT_PAID: "#15803d",
            Order.PAYMENT_FAILED: "#b91c1c",
            Order.PAYMENT_REFUNDED: "#4b5563",
        }
        return format_html(
            "<span class='sp-admin-badge' style='--badge-color:{}'>{}</span>",
            colors.get(obj.payment_status, "#6b7280"),
            obj.get_payment_status_display(),
        )

    @admin.display(description="Total")
    def total_display(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.get_total_cost()} FCFA"

    @admin.display(description="BAT visible client")
    def proof_file_link(self, obj):
        if not obj.proof_file:
            return "-"
        return format_html(
            "<a href='{}' target='_blank' rel='noopener'>{}</a>",
            obj.proof_file.url,
            obj.proof_file.name.split("/")[-1],
        )

    def update_payment_status(self, request, queryset, payment_status):
        updated = 0
        for order in queryset:
            order.payment_status = payment_status
            order.save(update_fields=["payment_status"])
            updated += 1
        self.message_user(request, f"{updated} commande(s) mise(s) a jour.")

    @admin.action(description="Marquer le paiement en attente")
    def mark_payment_pending(self, request, queryset):
        self.update_payment_status(request, queryset, Order.PAYMENT_PENDING)

    @admin.action(description="Marquer comme payé")
    def mark_payment_paid(self, request, queryset):
        self.update_payment_status(request, queryset, Order.PAYMENT_PAID)

    @admin.action(description="Marquer comme refusé")
    def mark_payment_failed(self, request, queryset):
        self.update_payment_status(request, queryset, Order.PAYMENT_FAILED)

    @admin.action(description="Marquer comme remboursé")
    def mark_payment_refunded(self, request, queryset):
        self.update_payment_status(request, queryset, Order.PAYMENT_REFUNDED)


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ["order", "previous_status", "new_status", "created_at"]
    list_filter = ["new_status", "created_at"]
    search_fields = ["order__id", "order__full_name", "note"]
    readonly_fields = ["order", "previous_status", "new_status", "note", "created_at"]
