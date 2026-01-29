from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, DashboardAnalysis, InvestmentPortfolio


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'created_at']


class DashboardAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardAnalysis
        fields = [
            'id', 'title', 'analysis_type', 'description', 
            'data', 'investor_only', 'created_at', 'updated_at', 'is_active'
        ]


class InvestmentPortfolioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = InvestmentPortfolio
        fields = ['id', 'username', 'name', 'total_value', 'currency', 'created_at', 'updated_at']
