from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_order_status_order_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="city",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="order",
            name="delivery_method",
            field=models.CharField(
                choices=[("pickup", "Retrait"), ("delivery", "Livraison")],
                default="pickup",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_provider",
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_reference",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("pending", "En attente"),
                    ("paid", "Payé"),
                    ("failed", "Échec"),
                    ("refunded", "Remboursé"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="phone",
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
