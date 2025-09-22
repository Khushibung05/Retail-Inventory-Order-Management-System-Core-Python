# src/dao/order_dao.py
from typing import Optional, List, Dict
from src.config import SupabaseConfig

class OrderDAO:
    """Data Access Object for orders and order_items."""

    def __init__(self):
        self.sb = SupabaseConfig.get_client()

    # ------------------ Orders ------------------
    def create_order(self, cust_id: int, total_amount: float) -> Dict:
        payload = {"cust_id": cust_id, "total_amount": total_amount}
        self.sb.table("orders").insert(payload).execute()
        resp = (
            self.sb.table("orders")
            .select("*")
            .eq("cust_id", cust_id)
            .order("order_id", desc=True)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        resp = self.sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_order_status(self, order_id: int, status: str) -> Optional[Dict]:
        self.sb.table("orders").update({"status": status}).eq("order_id", order_id).execute()
        return self.get_order_by_id(order_id)

    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        resp = self.sb.table("orders").select("*").eq("cust_id", cust_id).execute()
        return resp.data or []

    # ------------------ Order Items ------------------
    def create_order_item(self, order_id: int, prod_id: int, quantity: int, price: float) -> Dict:
        payload = {"order_id": order_id, "prod_id": prod_id, "quantity": quantity, "price": price}
        self.sb.table("order_items").insert(payload).execute()
        resp = (
            self.sb.table("order_items")
            .select("*")
            .eq("order_id", order_id)
            .eq("prod_id", prod_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def get_order_items(self, order_id: int) -> List[Dict]:
        resp = self.sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []
