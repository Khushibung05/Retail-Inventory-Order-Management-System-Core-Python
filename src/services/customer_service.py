from typing import List, Dict
from src.dao.customer_dao import CustomerDAO

class CustomerError(Exception):
    pass

class CustomerService:
    """Business logic for customers."""

    def __init__(self):
        self.repo = CustomerDAO()

    def add(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        if self.repo.get_by_email(email):
            raise CustomerError(f"Email already exists: {email}")
        return self.repo.create(name, email, phone, city)

    def list(self, limit: int = 100) -> List[Dict]:
        return self.repo.list(limit)

    def update(self, cust_id: int, phone: str | None = None, city: str | None = None) -> Dict:
        existing = self.repo.get_by_id(cust_id)
        if not existing:
            raise CustomerError("Customer not found")
        fields = {}
        if phone: fields["phone"] = phone
        if city: fields["city"] = city
        return self.repo.update(cust_id, fields)

    def delete(self, cust_id: int) -> Dict:
        existing = self.repo.get_by_id(cust_id)
        if not existing:
            raise CustomerError("Customer not found")
        return self.repo.delete(cust_id)

    def search(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        return self.repo.search(email=email, city=city)

    def get_by_id(self, cust_id: int) -> dict:
        customer = self.repo.get_by_id(cust_id)
        if not customer:
            raise CustomerError(f"Customer not found: {cust_id}")
        return customer
