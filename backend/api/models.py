from django.db import models
from django.contrib.auth.models import User

# User Profile with role-based access
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('investor', 'Investor'),
        ('user', 'Regular User'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def is_investor(self):
        return self.role == 'investor'
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


# Dashboard Analytics Base Model
class DashboardAnalysis(models.Model):
    ANALYSIS_TYPES = [
        ('portfolio_performance', 'Portfolio Performance Analysis'),
        ('risk_assessment', 'Risk Assessment'),
        ('market_trends', 'Market Trends'),
        ('roi_forecast', 'ROI Forecast'),
        ('investment_allocation', 'Investment Allocation'),
        ('comparative_analysis', 'Comparative Analysis'),
    ]
    
    title = models.CharField(max_length=200)
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPES)
    description = models.TextField()
    data = models.JSONField(help_text="JSON data containing analysis results")
    
    # Access control
    investor_only = models.BooleanField(
        default=False,
        help_text="If True, this analysis is only visible to investors"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        investor_tag = " [INVESTOR ONLY]" if self.investor_only else ""
        return f"{self.title}{investor_tag}"
    
    class Meta:
        verbose_name = 'Dashboard Analysis'
        verbose_name_plural = 'Dashboard Analyses'
        ordering = ['-updated_at']


# Investment Portfolio (for investor-specific data)
class InvestmentPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=200)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    class Meta:
        verbose_name = 'Investment Portfolio'
        verbose_name_plural = 'Investment Portfolios'
