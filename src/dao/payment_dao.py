from typing import Optional, Dict, List
from src.config import SupabaseConfig

class PaymentDAO:
    """Data-Access Object for payments table."""

    def __init__(self):
        self.sb = SupabaseConfig.get_client()

    def create_pending(self, order_id: int, amount: float) -> Optional[Dict]:
        payload = {"order_id": order_id, "amount": amount, "status": "PENDING", "method": None}
        self.sb.table("payments").insert(payload).execute()
        resp = self.sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_order(self, order_id: int) -> Optional[Dict]:
        resp = self.sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_status(self, order_id: int, status: str, method: str | None = None) -> Optional[Dict]:
        fields = {"status": status}
        if method:
            fields["method"] = method
        self.sb.table("payments").update(fields).eq("order_id", order_id).execute()
        return self.get_by_order(order_id)

    def list_by_status(self, status: str) -> List[Dict]:
        resp = self.sb.table("payments").select("*").eq("status", status).execute()
        return resp.data or []
