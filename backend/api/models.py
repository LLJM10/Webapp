from django.db import models
from django.conf import settings

# Erstelle deine Modelle hier
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Todo(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Pitch(models.Model):
    """
    Model to store startup pitches created by users.
    Each pitch is owned by a user (ForeignKey to AUTH_USER_MODEL).
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pitches',
        help_text='User who created this pitch'
    )
    title = models.CharField(max_length=200, help_text='Startup name or pitch title')
    sector = models.CharField(max_length=100, blank=True, help_text='Industry sector')
    stage = models.CharField(max_length=50, blank=True, help_text='Funding stage (e.g., Seed, Series A)')
    goal = models.CharField(max_length=64, blank=True, help_text='Funding goal (e.g., 500.000€)')
    equity = models.IntegerField(null=True, blank=True, help_text='Equity percentage offered')
    desc = models.TextField(blank=True, help_text='Pitch description')
    img = models.ImageField(upload_to='pitch_images/', blank=True, null=True, help_text='Pitch card image')
    valuation = models.CharField(max_length=64, blank=True, help_text='Calculated valuation')
    
    # PDF file uploads
    pitch_deck = models.FileField(
        upload_to='pitch_decks/',
        blank=True,
        null=True,
        help_text='Pitch Deck PDF file'
    )
    business_plan = models.FileField(
        upload_to='business_plans/',
        blank=True,
        null=True,
        help_text='Business Plan PDF file'
    )
    financial_report = models.FileField(
        upload_to='financial_reports/',
        blank=True,
        null=True,
        help_text='Financial Report PDF file'
    )
    
    is_public = models.BooleanField(default=True, help_text='Whether pitch is visible on marketplace')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pitch'
        verbose_name_plural = 'Pitches'

    def __str__(self):
        return f'{self.title} ({self.owner.username})'


class Event(models.Model):
    """
    Model to store events created by users.
    Each event is owned by a user (ForeignKey to AUTH_USER_MODEL).
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        help_text='User who created this event'
    )
    name = models.CharField(max_length=200, help_text='Event name')
    topic = models.CharField(max_length=200, help_text='Event topic or panel description')
    location = models.CharField(max_length=200, help_text='Location or platform (e.g., MS Teams, Zoom)')
    duration = models.IntegerField(help_text='Duration in minutes')
    date = models.DateTimeField(help_text='Event date and time')
    link = models.URLField(blank=True, help_text='Meeting link or registration URL')
    description = models.TextField(help_text='Detailed event description')
    img = models.ImageField(upload_to='event_images/', blank=True, null=True, help_text='Event cover image')
    host = models.CharField(max_length=200, blank=True, help_text='Host name or organization')
    is_public = models.BooleanField(default=True, help_text='Whether event is visible on marketplace')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']  # Order by event date (upcoming first)
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class SavedPitch(models.Model):
    """
    Model to store saved/bookmarked pitches by investors.
    Many-to-Many relationship between users and pitches.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_pitches',
        help_text='User who saved this pitch'
    )
    pitch = models.ForeignKey(
        Pitch,
        on_delete=models.CASCADE,
        related_name='saved_by',
        help_text='The saved pitch'
    )
    saved_at = models.DateTimeField(auto_now_add=True, help_text='When the pitch was saved')

    class Meta:
        unique_together = ('user', 'pitch')  # Prevent duplicate saves
        ordering = ['-saved_at']
        verbose_name = 'Saved Pitch'
        verbose_name_plural = 'Saved Pitches'

    def __str__(self):
        return f'{self.user.username} saved {self.pitch.title}'


class Investment(models.Model):
    """
    Model to track investments made by investors into pitches.
    Used for portfolio management, KPI calculations, and Value at Risk analysis.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('exited', 'Exited'),
        ('failed', 'Failed'),
    ]
    
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='investments',
        help_text='User who made the investment'
    )
    pitch = models.ForeignKey(
        Pitch,
        on_delete=models.CASCADE,
        related_name='investments',
        help_text='The pitch being invested in'
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        help_text='Investment amount in EUR'
    )
    equity_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text='Equity percentage acquired'
    )
    investment_date = models.DateTimeField(
        auto_now_add=True, 
        help_text='Date of investment'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        help_text='Current status of investment'
    )
    exit_date = models.DateTimeField(
        blank=True, 
        null=True,
        help_text='Date of exit (if applicable)'
    )
    exit_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text='Exit amount in EUR'
    )
    notes = models.TextField(blank=True, help_text='Investment notes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-investment_date']
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'
        constraints = [
            models.UniqueConstraint(fields=['investor', 'pitch'], name='unique_investor_pitch')
        ]

    def __str__(self):
        return f'{self.investor.username} → {self.pitch.title} ({self.amount}€)'
    
    @property
    def roi(self):
        """Calculate Return on Investment percentage"""
        if self.exit_amount and self.amount:
            return ((self.exit_amount - self.amount) / self.amount) * 100
        return None
    
    @property
    def current_value(self):
        """Return current value of investment"""
        if self.status == 'exited' and self.exit_amount:
            return self.exit_amount
        return self.amount  # For active investments, assume current value = investment amount

