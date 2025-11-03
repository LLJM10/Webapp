from django.db import models
from django.conf import settings

# Create your models here.
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
    img = models.URLField(blank=True, help_text='Image URL for pitch card')
    valuation = models.CharField(max_length=64, blank=True, help_text='Calculated valuation')
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
    img = models.URLField(blank=True, help_text='Event cover image URL')
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
