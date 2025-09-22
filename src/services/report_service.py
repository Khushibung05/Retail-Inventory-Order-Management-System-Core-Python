from datetime import datetime, timedelta
from typing import List, Dict
from src.dao.order_dao import OrderDAO
from src.dao.product_dao import ProductDAO
from src.dao.customer_dao import CustomerDAO

class ReportService:
    """Generate sales reports."""

    def __init__(self):
        self.order_dao = OrderDAO()
        self.product_dao = ProductDAO()
        self.customer_dao = CustomerDAO()

    def top_selling_products(self, top_n: int = 5) -> List[Dict]:
        items = self.order_dao.get_all_order_items()
        counts = {}
        for i in items:
            counts[i["prod_id"]] = counts.get(i["prod_id"], 0) + i["quantity"]
        top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        result = []
        for pid, qty in top:
            prod = self.product_dao.get_by_id(pid)
            result.append({"product": prod["name"], "quantity_sold": qty})
        return result

    def total_revenue_last_month(self) -> float:
        now = datetime.utcnow()
        last_month = now - timedelta(days=30)
        orders = self.order_dao.get_all_orders()
        total = sum(o["total_amount"] for o in orders if o["created_at"] >= last_month.isoformat())
        return total

    def orders_by_customer(self) -> List[Dict]:
        customers = self.customer_dao.list()
        result = []
        for c in customers:
            orders = self.order_dao.list_orders_by_customer(c["cust_id"])
            result.append({"customer": c["name"], "orders_count": len(orders)})
        return result

    def frequent_customers(self, min_orders: int = 2) -> List[Dict]:
        customers_orders = self.orders_by_customer()
        return [c for c in customers_orders if c["orders_count"] > min_orders]
