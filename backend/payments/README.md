# PayPal Integration (payments app)

Kurze Anleitung zur Entwicklung und Nutzung der PayPal-Backend-Komponenten.

Required environment variables (set in your environment or Docker):

- PAYPAL_MODE: `sandbox` oder `live` (default: sandbox)
- PAYPAL_CLIENT_ID
- PAYPAL_CLIENT_SECRET
- PAYPAL_WEBHOOK_ID (falls Webhook-Verifikation verwendet wird)

API Endpoints (registered under `/api/payments/`):

- `POST /api/payments/create-order/` (auth required)
  - body: {"amount": "10.00", "currency": "EUR", "return_url": "...", "cancel_url": "..."}
  - returns: {"order_id", "approval_url", "payment_id"}

- `POST /api/payments/capture-order/` (auth required)
  - body: {"order_id": "..."}
  - captures the order and updates Payment status

- `POST /api/payments/webhook/` (public)
  - PayPal will POST events here. We attempt to verify the signature and then update Payment records.

How to use locally:

1. Install dependencies: `pip install -r requirements.txt`
2. Set the PAYPAL_* env vars (sandbox credentials for testing).
3. Run: `python manage.py makemigrations payments` and `python manage.py migrate`
4. Create a superuser and open Django admin to inspect payments.

Notes:
- This is a minimal integration using `requests`. For production, consider using PayPal's official SDK and hardened error handling.
- Make sure to register the webhook URL in your PayPal developer dashboard and set PAYPAL_WEBHOOK_ID.
