from src.dao.payment_dao import PaymentDAO
from src.services.order_service import OrderService

class PaymentError(Exception):
    pass

class PaymentService:
    """Handles payments for orders."""

    def __init__(self):
        self.repo = PaymentDAO()
        self.order_service = OrderService()  # Only used for order status updates

    def create_pending_payment(self, order_id: int, amount: float):
        return self.repo.create(order_id, amount)

    def process_payment(self, order_id: int, method: str):
        payment = self.repo.get_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        if payment["status"] != "PENDING":
            raise PaymentError("Payment already processed")

        # Update payment
        self.repo.update_status(order_id, "PAID", method)

        # Complete order
        self.order_service.complete_order(order_id)
        return self.repo.get_by_order(order_id)

    def refund_payment(self, order_id: int):
        payment = self.repo.get_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        self.repo.update_status(order_id, "REFUNDED")
        return payment
