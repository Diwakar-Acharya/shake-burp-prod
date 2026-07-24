import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.orders.models import Order
from apps.payments.models import PaymentTransaction
from apps.payments.stripe_services import create_stripe_checkout_session, construct_stripe_webhook_event
from apps.orders.shiprocket import ShiprocketClient

logger = logging.getLogger(__name__)

def initiate_checkout_view(request, order_id):
    """Initiates a Stripe Checkout Session for a given order."""
    order = get_object_or_404(Order, id=order_id)
    domain_url = request.build_absolute_uri('/')[:-1]
    
    result = create_stripe_checkout_session(order, domain_url)
    if result.get("success"):
        # Record payment transaction
        PaymentTransaction.objects.create(
            order=order,
            stripe_checkout_session_id=result.get("session_id"),
            amount=order.total_amount,
            status='initiated'
        )
        return redirect(result.get("url"))
    else:
        return render(request, "pages/error.html", {"error": f"Failed to initiate payment: {result.get('error')}"})

def payment_success_view(request):
    """Renders payment success page."""
    session_id = request.GET.get("session_id")
    return render(request, "pages/payment_success.html", {"session_id": session_id})

def payment_cancel_view(request):
    """Renders payment cancel page."""
    return render(request, "pages/payment_cancel.html")

@csrf_exempt
@require_POST
def stripe_webhook_view(request):
    """Handles incoming Stripe webhooks for payment completion."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    event = construct_stripe_webhook_event(payload, sig_header)
    if not event:
        return HttpResponse(status=400)

    # Process checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('client_reference_id')
        payment_intent = session.get('payment_intent')
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'paid'
                order.save()

                # Update Payment Transaction
                tx = PaymentTransaction.objects.filter(order=order).last()
                if tx:
                    tx.stripe_payment_intent_id = payment_intent
                    tx.status = 'successful'
                    tx.save()

                # Trigger Shiprocket Order Creation
                sr_client = ShiprocketClient()
                sr_res = sr_client.create_order(order)
                if sr_res.get("success"):
                    data = sr_res.get("data", {})
                    order.shiprocket_order_id = str(data.get("order_id"))
                    order.shiprocket_shipment_id = str(data.get("shipment_id"))
                    order.save()
                    logger.info(f"Auto-created Shiprocket shipment for Order #{order.id}")

            except Order.DoesNotExist:
                logger.error(f"Webhook error: Order #{order_id} not found")

    return HttpResponse(status=200)
