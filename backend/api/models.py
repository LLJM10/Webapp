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
    Modell zum Speichern von Startup-Pitches, die von Benutzern erstellt wurden.
    Jeder Pitch gehört einem Benutzer (ForeignKey zu AUTH_USER_MODEL).
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pitches',
        help_text='Benutzer, der diesen Pitch erstellt hat'
    )
    title = models.CharField(max_length=200, help_text='Startup-Name oder Pitch-Titel')
    sector = models.CharField(max_length=100, blank=True, help_text='Branche')
    stage = models.CharField(max_length=50, blank=True, help_text='Finanzierungsphase (z.B. Seed, Series A)')
    goal = models.CharField(max_length=64, blank=True, help_text='Finanzierungsziel (z.B. 500.000€)')
    equity = models.IntegerField(null=True, blank=True, help_text='Angebotener Eigenkapitalanteil in Prozent')
    desc = models.TextField(blank=True, help_text='Pitch-Beschreibung')
    img = models.ImageField(upload_to='pitch_images/', blank=True, null=True, help_text='Pitch-Kartenbild')
    valuation = models.CharField(max_length=64, blank=True, help_text='Berechnete Bewertung')
    
    # PDF file uploads
    pitch_deck = models.FileField(
        upload_to='pitch_decks/',
        blank=True,
        null=True,
        help_text='Pitch-Deck-PDF-Datei'
    )
    business_plan = models.FileField(
        upload_to='business_plans/',
        blank=True,
        null=True,
        help_text='Businessplan-PDF-Datei'
    )
    financial_report = models.FileField(
        upload_to='financial_reports/',
        blank=True,
        null=True,
        help_text='Finanzbericht-PDF-Datei'
    )
    
    is_public = models.BooleanField(default=True, help_text='Ob Pitch auf Marktplatz sichtbar ist')
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
    Modell zum Speichern von Events, die von Benutzern erstellt wurden.
    Jedes Event gehört einem Benutzer (ForeignKey zu AUTH_USER_MODEL).
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        help_text='Benutzer, der dieses Event erstellt hat'
    )
    name = models.CharField(max_length=200, help_text='Event-Name')
    topic = models.CharField(max_length=200, help_text='Event-Thema oder Panel-Beschreibung')
    location = models.CharField(max_length=200, help_text='Ort oder Plattform (z.B. MS Teams, Zoom)')
    duration = models.IntegerField(help_text='Dauer in Minuten')
    date = models.DateTimeField(help_text='Event-Datum und -Zeit')
    link = models.URLField(blank=True, help_text='Meeting-Link oder Registrierungs-URL')
    description = models.TextField(help_text='Detaillierte Event-Beschreibung')
    img = models.ImageField(upload_to='event_images/', blank=True, null=True, help_text='Event-Titelbild')
    host = models.CharField(max_length=200, blank=True, help_text='Host-Name oder Organisation')
    is_public = models.BooleanField(default=True, help_text='Ob Event auf Marktplatz sichtbar ist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']  # Nach Event-Datum sortieren (anstehende zuerst)
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class SavedPitch(models.Model):
    """
    Modell zum Speichern von gespeicherten/gemerkten Pitches durch Investoren.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_pitches',
        help_text='Benutzer, der diesen Pitch gespeichert hat'
    )
    pitch = models.ForeignKey(
        Pitch,
        on_delete=models.CASCADE,
        related_name='saved_by',
        help_text='Der gespeicherte Pitch'
    )
    saved_at = models.DateTimeField(auto_now_add=True, help_text='Wann der Pitch gespeichert wurde')

    class Meta:
        unique_together = ('user', 'pitch')  # Verhindere doppelte Speicherungen
        ordering = ['-saved_at']
        verbose_name = 'Saved Pitch'
        verbose_name_plural = 'Saved Pitches'

    def __str__(self):
        return f'{self.user.username} saved {self.pitch.title}'


class Investment(models.Model):
    """
    Modell zum Verfolgen von Investitionen durch Investoren in Pitches.
    Wird für Portfolio-Management, KPI-Berechnungen und Value-at-Risk-Analysen verwendet.
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
        help_text='Benutzer, der die Investition getätigt hat'
    )
    pitch = models.ForeignKey(
        Pitch,
        on_delete=models.CASCADE,
        related_name='investments',
        help_text='Der Pitch, in den investiert wird'
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        help_text='Investitionsbetrag in EUR'
    )
    equity_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text='Erworbener Eigenkapitalanteil'
    )
    investment_date = models.DateTimeField(
        auto_now_add=True, 
        help_text='Datum der Investition'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        help_text='Aktueller Status der Investition'
    )
    exit_date = models.DateTimeField(
        blank=True, 
        null=True,
        help_text='Datum des Ausstiegs (falls zutreffend)'
    )
    exit_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text='Ausstiegsbetrag in EUR'
    )
    notes = models.TextField(blank=True, help_text='Investitionsnotizen')
    
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
        """Berechnet den Return on Investment in Prozent"""
        if self.exit_amount and self.amount:
            return ((self.exit_amount - self.amount) / self.amount) * 100
        return None
    
    @property
    def current_value(self):
        """Gibt aktuellen Wert der Investition zurück"""
        if self.status == 'exited' and self.exit_amount:
            return self.exit_amount
        return self.amount  # Für aktive Investitionen, nehme aktuellen Wert = Investitionsbetrag

