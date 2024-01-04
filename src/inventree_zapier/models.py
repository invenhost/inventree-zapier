"""Models for ZapierPlugin."""
from django.db import models


class EventRegistration(models.Model):
    """Keeps a list of all registered events."""

    event = models.CharField(
        max_length=250,
    )
    model = models.CharField(
        max_length=250,
    )

    def __str__(self):
        """Get string representation of event."""
        return str(self.event)


class ZapierHook(models.Model):
    """Keeps a list of all registered zaier callback hooks."""

    hookurl = models.CharField(
        max_length=250,
    )

    def __str__(self):
        """Get string representation of hook."""
        return str(self.hookurl)
