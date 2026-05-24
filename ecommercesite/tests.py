from django.test import TestCase

from orders.models import Order

from .admin_dashboard import build_admin_dashboard_context


class AdminDashboardContextTests(TestCase):
    def create_order(self, payment_status):
        return Order.objects.create(
            full_name="Client Test",
            phone="+221770000000",
            email="client@example.com",
            address="Dakar",
            city="Dakar",
            payment_status=payment_status,
        )

    def test_dashboard_counts_payment_statuses_not_production_pending(self):
        self.create_order(Order.PAYMENT_PENDING)
        self.create_order(Order.PAYMENT_PAID)
        self.create_order(Order.PAYMENT_PAID)
        self.create_order(Order.PAYMENT_REFUNDED)

        dashboard = build_admin_dashboard_context()["sp_dashboard"]

        self.assertEqual(dashboard["orders_total"], 4)
        self.assertEqual(dashboard["orders_pending"], 4)
        self.assertEqual(dashboard["payments_pending"], 1)
        self.assertEqual(dashboard["payments_paid"], 2)
