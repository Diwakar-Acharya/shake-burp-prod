import logging
import stripe
from django.conf import settings

logger = logging.getLogger(__name__)

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

def create_stripe_checkout_session(order, domain_url: str) -> dict:
    """Creates a Stripe Checkout Session for a Django Order."""
    try:
        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product_name,
                    },
                    'unit_amount': int(item.price * 100),  # Stripe uses cents
                },
                'quantity': item.quantity,
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            customer_email=order.email,
            client_reference_id=str(order.id),
            success_url=f"{domain_url}/checkout/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain_url}/checkout/cancel/",
        )
        return {"success": True, "session_id": session.id, "url": session.url}
    except Exception as e:
        logger.error(f"Failed to create Stripe checkout session: {str(e)}")
        return {"success": False, "error": str(e)}

def construct_stripe_webhook_event(payload, sig_header):
    """Verifies and constructs a Stripe Webhook Event."""
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        return event
    except ValueError:
        logger.error("Invalid Stripe payload")
        return None
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid Stripe signature")
        return None
