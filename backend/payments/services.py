import requests
from django.conf import settings


class PayPalClient:
    """Minimaler PayPal HTTP Client ohne externes SDK.

    Verwendet Client-Anmeldedaten um ein OAuth2-Token zu erhalten und bietet
    Hilfsfunktionen zum Erstellen und Abschließen von Bestellungen. Dies ist
    absichtlich klein und ohne Abhängigkeiten (nutzt requests). In der Produktion
    sollte das offizielle SDK mit robuster Fehlerbehandlung verwendet werden.
    """

    def __init__(self):
        mode = getattr(settings, 'PAYPAL_MODE', 'sandbox')
        if mode == 'live':
            self.base = 'https://api-m.paypal.com'
        else:
            self.base = 'https://api-m.sandbox.paypal.com'
        # Lese Anmeldedaten aus den Settings (in Produktion über Umgebungsvariablen setzen)
        self.client_id = getattr(settings, 'PAYPAL_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'PAYPAL_CLIENT_SECRET', '')
        if not self.client_id or not self.client_secret:
            # Schnell fehlschlagen mit klarer Meldung wenn Anmeldedaten fehlen
            raise ValueError('PayPal client credentials are not configured (PAYPAL_CLIENT_ID / PAYPAL_CLIENT_SECRET)')

    def _get_access_token(self):
        url = f"{self.base}/v1/oauth2/token"
        resp = requests.post(url, data={'grant_type': 'client_credentials'}, auth=(self.client_id, self.client_secret))
        resp.raise_for_status()
        return resp.json().get('access_token')

    def create_order(self, amount: str, currency: str = 'EUR', return_url: str = '', cancel_url: str = ''):
        token = self._get_access_token()
        url = f"{self.base}/v2/checkout/orders"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        body = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(amount)
                    }
                }
            ]
        }
        if return_url and cancel_url:
            body['application_context'] = {
                'return_url': return_url,
                'cancel_url': cancel_url,
            }

        resp = requests.post(url, json=body, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def capture_order(self, order_id: str):
        token = self._get_access_token()
        url = f"{self.base}/v2/checkout/orders/{order_id}/capture"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        resp = requests.post(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def verify_webhook_signature(self, transmission_id, timestamp, webhook_id, event_body, cert_url, auth_algo, transmission_sig):
        # Verwendet PayPal verify-webhook-signature Endpunkt. Benötigt webhook_id in den Settings.
        token = self._get_access_token()
        url = f"{self.base}/v1/notifications/verify-webhook-signature"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        payload = {
            'transmission_id': transmission_id,
            'transmission_time': timestamp,
            'cert_url': cert_url,
            'auth_algo': auth_algo,
            'transmission_sig': transmission_sig,
            'webhook_id': getattr(settings, 'PAYPAL_WEBHOOK_ID', ''),
            'webhook_event': event_body,
        }
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
