from typing import List, Dict
from src.dao.order_dao import OrderDAO
from src.services.customer_service import CustomerService
from src.services.product_service import ProductService

class OrderError(Exception):
    pass

class OrderService:
    """Business logic for orders."""

    def __init__(self):
        self.repo = OrderDAO()
        self.customer_service = CustomerService()
        self.product_service = ProductService()
        # PaymentService is NOT imported here to avoid circular imports

    def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
        # Check customer exists
        customer = self.customer_service.get_by_id(cust_id)

        # Check product stock & calculate total
        total_amount = 0
        for item in items:
            prod = self.product_service.get_by_id(item["prod_id"])
            if prod["stock"] < item["quantity"]:
                raise OrderError(f"Not enough stock for {prod['name']} (available: {prod['stock']})")
            total_amount += prod["price"] * item["quantity"]

        # Create order
        order = self.repo.create_order(cust_id, total_amount)

        # Deduct stock and create order_items
        for item in items:
            prod = self.product_service.get_by_id(item["prod_id"])
            self.product_service.update(prod["prod_id"], stock=prod["stock"] - item["quantity"])
            self.repo.create_order_item(order["order_id"], prod["prod_id"], item["quantity"], prod["price"])

        return self.get_order_details(order["order_id"])

    def get_order_details(self, order_id: int) -> Dict:
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        customer = self.customer_service.get_by_id(order["cust_id"])
        items = self.repo.get_order_items(order_id)
        return {"order": order, "customer": customer, "items": items}

    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        return self.repo.list_orders_by_customer(cust_id)

    def cancel_order(self, order_id: int) -> Dict:
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        if order["status"] != "PLACED":
            raise OrderError("Only orders with status PLACED can be cancelled")

        # Restore stock
        items = self.repo.get_order_items(order_id)
        for item in items:
            prod = self.product_service.get_by_id(item["prod_id"])
            self.product_service.update(prod["prod_id"], stock=prod["stock"] + item["quantity"])

        # Update order status
        return self.repo.update_order_status(order_id, "CANCELLED")

    def complete_order(self, order_id: int) -> Dict:
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        if order["status"] != "PLACED":
            raise OrderError("Only orders with status PLACED can be completed")
        return self.repo.update_order_status(order_id, "COMPLETED")
