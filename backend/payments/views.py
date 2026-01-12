from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .services import PayPalClient
from .models import Payment
from .serializers import PaymentSerializer
import logging

logger = logging.getLogger(__name__)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """PayPal-Bestellung für angegebenen Betrag und Währung.

        Anfrage-JSON: {"amount": "10.00", "currency": "EUR", "return_url": "...", "cancel_url": "..."}
        """
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'EUR')
        return_url = request.data.get('return_url', '')
        cancel_url = request.data.get('cancel_url', '')

        if not amount:
            return Response({'detail': 'amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = PayPalClient()
            data = client.create_order(amount, currency, return_url, cancel_url)
        except Exception as e:
            logger.exception('Error creating PayPal order')
            return Response({'detail': 'Failed to create PayPal order', 'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        order_id = data.get('id')
        # Zahlungsdatensatz speichern
        payment = Payment.objects.create(
            user=request.user,
            order_id=order_id,
            amount=amount,
            currency=currency,
            status='CREATED',
            raw_response=data,
        )

        # Finde Genehmigungs-URL
        approval_url = None
        for link in data.get('links', []):
            if link.get('rel') == 'approve' or link.get('rel') == 'approval_url':
                approval_url = link.get('href')

        return Response({'order_id': order_id, 'approval_url': approval_url, 'payment_id': payment.id})


class CaptureOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'detail': 'order_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = PayPalClient()
            data = client.capture_order(order_id)
        except Exception as e:
            logger.exception('Error capturing PayPal order %s', order_id)
            return Response({'detail': 'Failed to capture PayPal order', 'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # Aktualisiere Zahlung
        try:
            payment = Payment.objects.get(order_id=order_id)
        except Payment.DoesNotExist:
            payment = None

        if payment:
            captures = []
            for pu in data.get('purchase_units', []):
                payments = pu.get('payments', {})
                captures.extend(payments.get('captures', []))
            capture_id = captures[0].get('id') if captures else None
            payment.capture_id = capture_id
            payment.status = 'COMPLETED'
            payment.raw_response = data
            payment.save()

        return Response({'status': 'completed', 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        #Signatur verifizieren und Events verarbeiten
        client = PayPalClient()

        transmission_id = request.META.get('HTTP_PAYPAL_TRANSMISSION_ID')
        timestamp = request.META.get('HTTP_PAYPAL_TRANSMISSION_TIME')
        cert_url = request.META.get('HTTP_PAYPAL_CERT_URL')
        auth_algo = request.META.get('HTTP_PAYPAL_AUTH_ALGO')
        transmission_sig = request.META.get('HTTP_PAYPAL_TRANSMISSION_SIG')

        try:
            verification = client.verify_webhook_signature(
                transmission_id, timestamp, settings.PAYPAL_WEBHOOK_ID, request.data,
                cert_url, auth_algo, transmission_sig
            )
        except Exception as e:
            # Wenn Verifizierung fehlschlägt
            return Response({'detail': 'verification failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if verification.get('verification_status') != 'SUCCESS':
            return Response({'detail': 'invalid webhook signature'}, status=status.HTTP_400_BAD_REQUEST)

        event_type = request.data.get('event_type')
        resource = request.data.get('resource', {})

        # Häufige Events verarbeiten
        if event_type == 'CHECKOUT.ORDER.APPROVED':
            order_id = resource.get('id')
            Payment.objects.filter(order_id=order_id).update(status='APPROVED', raw_response=resource)

        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            # Resource enthält Capture-Details
            order_id = resource.get('supplementary_data', {}).get('related_ids', {}).get('order_id')
            capture_id = resource.get('id')
            Payment.objects.filter(order_id=order_id).update(status='COMPLETED', capture_id=capture_id, raw_response=resource)

        return Response({'status': 'ok'})
