from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import UserProfile, DashboardAnalysis, InvestmentPortfolio


class Command(BaseCommand):
    help = 'Populates the database with sample dashboard analyses and user data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with sample data...')
        
        # Create users with different roles
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserProfile.objects.create(user=admin_user, role='admin')
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin'))
        
        investor_user, created = User.objects.get_or_create(
            username='investor1',
            defaults={'email': 'investor@example.com'}
        )
        if created:
            investor_user.set_password('investor123')
            investor_user.save()
            UserProfile.objects.create(user=investor_user, role='investor')
            self.stdout.write(self.style.SUCCESS(f'Created investor user: investor1'))
        
        regular_user, created = User.objects.get_or_create(
            username='user1',
            defaults={'email': 'user@example.com'}
        )
        if created:
            regular_user.set_password('user123')
            regular_user.save()
            UserProfile.objects.create(user=regular_user, role='user')
            self.stdout.write(self.style.SUCCESS(f'Created regular user: user1'))
        
        # Create public analyses (visible to all users)
        public_analyses = [
            {
                'title': 'Marktübersicht',
                'analysis_type': 'market_trends',
                'description': 'Allgemeine Markttrends und Übersichten',
                'investor_only': False,
                'data': {
                    'trend': 'positive',
                    'market_cap': '1.5T EUR',
                    'daily_volume': '50B EUR'
                }
            },
            {
                'title': 'Wirtschaftsindikatoren',
                'analysis_type': 'market_trends',
                'description': 'Wichtige wirtschaftliche Kennzahlen und Indikatoren',
                'investor_only': False,
                'data': {
                    'gdp_growth': '2.5%',
                    'inflation': '2.1%',
                    'unemployment': '3.8%'
                }
            }
        ]
        
        for analysis_data in public_analyses:
            obj, created = DashboardAnalysis.objects.get_or_create(
                title=analysis_data['title'],
                defaults=analysis_data
            )
            if created:
                self.stdout.write(f'Created public analysis: {obj.title}')
        
        # Create investor-only analyses
        investor_analyses = [
            {
                'title': 'Portfolio Performance Analyse',
                'analysis_type': 'portfolio_performance',
                'description': 'Detaillierte Analyse der Portfolio-Performance mit historischen Daten',
                'investor_only': True,
                'data': {
                    'total_return': '15.3%',
                    'ytd_return': '8.7%',
                    'sharpe_ratio': '1.85',
                    'volatility': '12.4%',
                    'top_performers': ['AAPL', 'MSFT', 'GOOGL']
                }
            },
            {
                'title': 'Risikobewertung',
                'analysis_type': 'risk_assessment',
                'description': 'Umfassende Risikobewertung mit VaR und Stress-Tests',
                'investor_only': True,
                'data': {
                    'value_at_risk': '-5.2%',
                    'expected_shortfall': '-7.8%',
                    'risk_grade': 'B+',
                    'stress_test_results': {
                        'market_crash': '-15%',
                        'interest_rate_shock': '-8%'
                    }
                }
            },
            {
                'title': 'ROI-Prognose',
                'analysis_type': 'roi_forecast',
                'description': 'Erwartete Rendite-Prognosen für die nächsten 12 Monate',
                'investor_only': True,
                'data': {
                    'forecast_12m': '12-18%',
                    'confidence_level': '85%',
                    'best_case': '22%',
                    'worst_case': '4%',
                    'expected_return': '14.5%'
                }
            },
            {
                'title': 'Investitionsallokation',
                'analysis_type': 'investment_allocation',
                'description': 'Optimierte Asset-Allocation-Strategie',
                'investor_only': True,
                'data': {
                    'stocks': '60%',
                    'bonds': '25%',
                    'real_estate': '10%',
                    'commodities': '5%',
                    'rebalancing_needed': False
                }
            },
            {
                'title': 'Vergleichsanalyse',
                'analysis_type': 'comparative_analysis',
                'description': 'Vergleich mit Benchmark-Indizes und Peer-Portfolios',
                'investor_only': True,
                'data': {
                    'vs_sp500': '+3.2%',
                    'vs_dax': '+5.7%',
                    'vs_peer_average': '+2.1%',
                    'ranking': 'Top 15%'
                }
            },
            {
                'title': 'Erweiterte Kennzahlen',
                'analysis_type': 'portfolio_performance',
                'description': 'Detaillierte Performance-Metriken für Investoren',
                'investor_only': True,
                'data': {
                    'alpha': '2.3%',
                    'beta': '1.12',
                    'treynor_ratio': '0.18',
                    'information_ratio': '0.65',
                    'max_drawdown': '-18.5%'
                }
            }
        ]
        
        for analysis_data in investor_analyses:
            obj, created = DashboardAnalysis.objects.get_or_create(
                title=analysis_data['title'],
                defaults=analysis_data
            )
            if created:
                self.stdout.write(self.style.WARNING(f'Created INVESTOR-ONLY analysis: {obj.title}'))
        
        # Create sample portfolios for investor
        if hasattr(investor_user, 'profile') and investor_user.profile.is_investor():
            portfolio, created = InvestmentPortfolio.objects.get_or_create(
                user=investor_user,
                name='Hauptportfolio',
                defaults={
                    'total_value': 250000.00,
                    'currency': 'EUR'
                }
            )
            if created:
                self.stdout.write(f'Created portfolio for {investor_user.username}')
        
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.WARNING('\n⚠️  TEST CREDENTIALS (DO NOT USE IN PRODUCTION):'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Investor: investor1 / investor123')
        self.stdout.write('  Regular User: user1 / user123')
        self.stdout.write(self.style.WARNING('\nThese are development/testing credentials only.'))
        self.stdout.write(self.style.WARNING('Change all passwords before deploying to production!\n'))
        self.stdout.write(self.style.SUCCESS(f'Investor-Only Analyses: {len(investor_analyses)}'))
        self.stdout.write(self.style.SUCCESS(f'Public Analyses: {len(public_analyses)}'))
