from django.db import migrations, models


def populate_order_numbers(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    for order in Order.objects.order_by("id"):
        if order.order_number:
            continue
        year = order.created_at.year if order.created_at else 2026
        order.order_number = f"SPT-{year}-{order.id:06d}"
        order.save(update_fields=["order_number"])


def clear_order_numbers(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.update(order_number=None)


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_order_payment_method_payment_status_labels"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_number",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=20,
                null=True,
                unique=True,
            ),
        ),
        migrations.RunPython(populate_order_numbers, clear_order_numbers),
    ]
