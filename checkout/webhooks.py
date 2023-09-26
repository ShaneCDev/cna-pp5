from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listen to webhooks from stripe"""
    # setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)
    
    # setup wh handler
    handler = StripeWH_Handler(request)

    # map wh events to relevant functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_suceeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # get wh type from stripe
    event_type = event['type']

    # if theres a handler get it from event map
    # use generic by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # call event handler
    response = event_handler(event)
    return response
