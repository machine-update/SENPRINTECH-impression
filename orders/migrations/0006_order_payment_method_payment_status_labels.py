from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_order_assigned_to_order_internal_notes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("wave", "Wave"),
                    ("orange_money", "Orange Money"),
                    ("card", "Carte bancaire (bientot)"),
                ],
                default="wave",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("pending", "En attente"),
                    ("paid", "Paye"),
                    ("failed", "Refuse"),
                    ("refunded", "Rembourse"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
