from django.db import models
from django.conf import settings


class Todo(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Pitch(models.Model):
    """Startup-Pitches mit Finanzierungs-Details"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pitches'
    )
    title = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=50, blank=True, help_text='z.B. Seed, Series A')
    goal = models.CharField(max_length=64, blank=True)
    equity = models.IntegerField(null=True, blank=True, help_text='Anteil in %')
    desc = models.TextField(blank=True)
    img = models.ImageField(upload_to='pitch_images/', blank=True, null=True)
    valuation = models.CharField(max_length=64, blank=True)
    
    pitch_deck = models.FileField(upload_to='pitch_decks/', blank=True, null=True)
    business_plan = models.FileField(upload_to='business_plans/', blank=True, null=True)
    financial_report = models.FileField(upload_to='financial_reports/', blank=True, null=True)
    
    is_public = models.BooleanField(default=True, help_text='Sichtbar auf Marktplatz')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pitch'
        verbose_name_plural = 'Pitches'

    def __str__(self):
        return f'{self.title} ({self.owner.username})'


class Event(models.Model):
    """Networking-Events und Veranstaltungen"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text='z.B. MS Teams, Zoom')
    duration = models.IntegerField(help_text='in Minuten')
    date = models.DateTimeField()
    link = models.URLField(blank=True)
    description = models.TextField()
    img = models.ImageField(upload_to='event_images/', blank=True, null=True)
    host = models.CharField(max_length=200, blank=True)
    is_public = models.BooleanField(default=True, help_text='Sichtbar auf Marktplatz')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class SavedPitch(models.Model):
    """Gemerkte Pitches (Watchlist)"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_pitches'
    )
    pitch = models.ForeignKey(
        Pitch,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pitch')
        ordering = ['-saved_at']
        verbose_name = 'Saved Pitch'
        verbose_name_plural = 'Saved Pitches'

    def __str__(self):
        return f'{self.user.username} saved {self.pitch.title}'


class Investment(models.Model):
    """Portfolio-Investitionen mit ROI-Tracking"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('exited', 'Exited'),
        ('failed', 'Failed'),
    ]
    
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='investments'
    )
    pitch = models.ForeignKey(
        Pitch,
        on_delete=models.CASCADE,
        related_name='investments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text='in EUR')
    equity_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Erworbener Anteil in %'
    )
    investment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    exit_date = models.DateTimeField(blank=True, null=True, help_text='bei Exit/Verkauf')
    exit_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text='in EUR')
    notes = models.TextField(blank=True)
    
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
        """Return on Investment in %"""
        if self.exit_amount and self.amount:
            return ((self.exit_amount - self.amount) / self.amount) * 100
        return None
    
    @property
    def current_value(self):
        """Aktueller Wert"""
        if self.status == 'exited' and self.exit_amount:
            return self.exit_amount
        return self.amount

