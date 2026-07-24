import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class ShiprocketClient:
    BASE_URL = "https://apiv2.shiprocket.in/v1/external"

    def __init__(self):
        self.email = getattr(settings, 'SHIPROCKET_EMAIL', '')
        self.password = getattr(settings, 'SHIPROCKET_PASSWORD', '')
        self.token = None

    def authenticate(self) -> str:
        """Authenticate with Shiprocket API to retrieve a Bearer Token."""
        if not self.email or not self.password:
            logger.warning("Shiprocket credentials not provided.")
            return ""

        url = f"{self.BASE_URL}/auth/login"
        payload = {"email": self.email, "password": self.password}
        try:
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                self.token = res.json().get("token")
                return self.token
            else:
                logger.error(f"Shiprocket auth failed: {res.status_code} - {res.text}")
        except Exception as e:
            logger.error(f"Shiprocket auth exception: {str(e)}")
        return ""

    def create_order(self, order) -> dict:
        """Pushes Django Order details to Shiprocket for fulfillment."""
        if not self.token:
            self.authenticate()
        if not self.token:
            return {"success": False, "error": "Authentication failed"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        items = []
        for item in order.items.all():
            items.append({
                "name": item.product_name,
                "sku": f"PROD-{item.id}",
                "units": item.quantity,
                "selling_price": float(item.price),
                "discount": 0,
                "tax": 0,
            })

        payload = {
            "order_id": f"SB-ORD-{order.id}",
            "order_date": order.created_at.strftime("%Y-%m-%d %H:%M"),
            "pickup_location": "Primary",
            "billing_customer_name": order.first_name,
            "billing_last_name": order.last_name,
            "billing_address": order.address,
            "billing_city": order.city,
            "billing_pincode": order.postal_code,
            "billing_state": "Maharashtra",
            "billing_country": order.country,
            "billing_email": order.email,
            "billing_phone": "9999999999",
            "shipping_is_billing": True,
            "order_items": items,
            "payment_method": "Prepaid",
            "sub_total": float(order.total_amount),
            "length": 10,
            "breadth": 10,
            "height": 15,
            "weight": 0.5
        }

        url = f"{self.BASE_URL}/orders/create/adhoc"
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                logger.info(f"Shiprocket order created: {data.get('order_id')}")
                return {"success": True, "data": data}
            else:
                logger.error(f"Shiprocket order creation failed: {res.text}")
                return {"success": False, "error": res.text}
        except Exception as e:
            logger.error(f"Shiprocket order creation exception: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_tracking(self, shipment_id: str) -> dict:
        """Retrieves real-time shipment tracking details."""
        if not self.token:
            self.authenticate()
        if not self.token:
            return {}

        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.BASE_URL}/courier/track/shipment/{shipment_id}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                return res.json()
        except Exception as e:
            logger.error(f"Shiprocket tracking error: {str(e)}")
        return {}
