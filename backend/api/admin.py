from django.contrib import admin

# Register your models here.
from .models import MyModel, Todo, Pitch, Event, SavedPitch, Investment

admin.site.register(MyModel)
admin.site.register(Todo)
admin.site.register(Pitch)
admin.site.register(Event)
admin.site.register(SavedPitch)


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investor', 'pitch', 'amount', 'status', 'investment_date', 'roi']
    list_filter = ['status', 'investment_date']
    search_fields = ['investor__username', 'pitch__title']
    readonly_fields = ['investment_date', 'created_at', 'updated_at', 'roi', 'current_value']
    
    fieldsets = (
        ('Investment Details', {
            'fields': ('investor', 'pitch', 'amount', 'equity_percentage', 'status')
        }),
        ('Dates', {
            'fields': ('investment_date', 'exit_date')
        }),
        ('Exit Information', {
            'fields': ('exit_amount', 'roi', 'current_value'),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
