from django.conf import settings
from django.db import models
import math

from accounts.models import UserProfile


class Quest(models.Model):
    STATUS_OPEN = "open"
    STATUS_ASSIGNED = "assigned"
    STATUS_COMPLETED = "completed"
    STATUS_PAID = "paid"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_PAID, "Paid"),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_quests"
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="worker_quests",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.CharField(
        max_length=20, choices=UserProfile.SERVICE_TYPE_CHOICES
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN
    )

    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    review = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.title

    def can_be_accepted_by(self, profile: UserProfile) -> bool:
        if self.status != self.STATUS_OPEN:
            return False
        if not profile.can_accept_more_quests:
            return False
        # Prevent the client who posted the quest from accepting it
        if profile.user == self.client:
            return False
        if profile.service_type and profile.service_type != self.service_type:
            return False
        # If the quest requires physical presence, enforce a distance limit
        if self.service_type == UserProfile.SERVICE_PHYSICAL:
            # Need both quest and profile coordinates to check distance
            if self.latitude is None or self.longitude is None:
                return False
            if profile.latitude is None or profile.longitude is None:
                return False
            # compute distance in kilometers
            dist_km = self._haversine_km(profile.latitude, profile.longitude, self.latitude, self.longitude)
            return dist_km <= 10.0
        return True

    @staticmethod
    def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Return distance between two lat/lon points in kilometers."""
        # convert decimal degrees to radians
        rlat1, rlon1, rlat2, rlon2 = map(math.radians, (lat1, lon1, lat2, lon2))
        dlat = rlat2 - rlat1
        dlon = rlon2 - rlon1
        a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        R = 6371.0  # Earth radius in kilometers
        return R * c

