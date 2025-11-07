from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'amount', 'currency', 'status', 'created_at')
    search_fields = ('order_id', 'capture_id', 'user__username')
    readonly_fields = ('raw_response',)
