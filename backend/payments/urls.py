from django.urls import path
from .views import CreateOrderView, CaptureOrderView, WebhookView

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='paypal-create-order'),
    path('capture-order/', CaptureOrderView.as_view(), name='paypal-capture-order'),
    path('webhook/', WebhookView.as_view(), name='paypal-webhook'),
]
