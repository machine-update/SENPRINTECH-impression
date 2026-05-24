from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0007_order_order_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("pending", "En attente"),
                    ("paid", "Payé"),
                    ("failed", "Refusé"),
                    ("refunded", "Remboursé"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
