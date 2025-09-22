from typing import Optional, List, Dict
from src.config import SupabaseConfig


class CustomerDAO:
    """Data-access object for customers table."""

    def __init__(self):
        self.sb = SupabaseConfig.get_client()

    def create(self, name: str, email: str, phone: str, city: str | None = None) -> Optional[Dict]:
        # Check uniqueness of email
        if self.get_by_email(email):
            return None
        payload = {"name": name, "email": email, "phone": phone}
        if city:
            payload["city"] = city
        self.sb.table("customers").insert(payload).execute()
        resp = self.sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self.sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_email(self, email: str) -> Optional[Dict]:
        resp = self.sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        self.sb.table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self.sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete(self, cust_id: int) -> Optional[Dict]:
        # Check if customer has orders
        orders = self.sb.table("orders").select("*").eq("cust_id", cust_id).execute()
        if orders.data:
            raise Exception("Cannot delete customer with existing orders")
        before = self.sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = before.data[0] if before.data else None
        self.sb.table("customers").delete().eq("cust_id", cust_id).execute()
        return row

    def list(self, limit: int = 100) -> List[Dict]:
        resp = self.sb.table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []

    def search(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        q = self.sb.table("customers").select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []
