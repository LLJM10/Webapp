from django.contrib import admin
from .models import UserProfile, DashboardAnalysis, InvestmentPortfolio


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(DashboardAnalysis)
class DashboardAnalysisAdmin(admin.ModelAdmin):
    list_display = ['title', 'analysis_type', 'investor_only', 'is_active', 'updated_at']
    list_filter = ['investor_only', 'is_active', 'analysis_type']
    search_fields = ['title', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'analysis_type', 'description')
        }),
        ('Data', {
            'fields': ('data',)
        }),
        ('Access Control', {
            'fields': ('investor_only', 'is_active')
        }),
    )


@admin.register(InvestmentPortfolio)
class InvestmentPortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total_value', 'currency', 'updated_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['name', 'user__username']
