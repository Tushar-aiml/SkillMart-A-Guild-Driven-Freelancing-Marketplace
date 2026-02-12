from django.conf import settings
from django.db import models

from marketplace.models import Quest


class Payment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
    ]

    quest = models.OneToOneField(Quest, on_delete=models.CASCADE, related_name="payment")
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments_made"
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments_received",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Payment for {self.quest.title}"

