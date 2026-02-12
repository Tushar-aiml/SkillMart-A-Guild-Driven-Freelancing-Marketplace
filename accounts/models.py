from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CLIENT = "client"
    ROLE_WORKER = "worker"
    ROLE_BOTH = "both"

    SERVICE_PHYSICAL = "physical"
    SERVICE_VIRTUAL = "virtual"
    SERVICE_TYPE_CHOICES = [
        (SERVICE_PHYSICAL, "Physical"),
        (SERVICE_VIRTUAL, "Virtual"),
    ]

    RANK_BEGINNER = "Beginner"
    RANK_INTERMEDIATE = "Intermediate"
    RANK_ADVANCED = "Advanced"
    RANK_EXPERT = "Expert"
    RANK_MASTER = "Master"

    RANK_CHOICES = [
        (RANK_BEGINNER, "Beginner"),
        (RANK_INTERMEDIATE, "Intermediate"),
        (RANK_ADVANCED, "Advanced"),
        (RANK_EXPERT, "Expert"),
        (RANK_MASTER, "Master"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default=ROLE_BOTH)
    service_type = models.CharField(
        max_length=20, choices=SERVICE_TYPE_CHOICES, blank=True
    )
    skills = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    bio = models.TextField(blank=True)

    # Progression fields
    exp = models.PositiveIntegerField(default=0)
    rank = models.CharField(
        max_length=20, choices=RANK_CHOICES, default=RANK_BEGINNER
    )
    completed_quests = models.PositiveIntegerField(default=0)

    # Premium / membership
    is_premium = models.BooleanField(default=False)
    premium_since = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username}"

    @staticmethod
    def rank_for_exp(exp: int) -> str:
        """Determine rank based on EXP thresholds."""
        if exp >= 1000:
            return UserProfile.RANK_MASTER
        if exp >= 600:
            return UserProfile.RANK_EXPERT
        if exp >= 350:
            return UserProfile.RANK_ADVANCED
        if exp >= 150:
            return UserProfile.RANK_INTERMEDIATE
        return UserProfile.RANK_BEGINNER

    def add_exp_for_completed_quest(self, base_exp: int = 50) -> None:
        """Increase EXP and adjust rank; premium members gain faster EXP."""
        multiplier = 1.5 if self.is_premium else 1.0
        gained = int(base_exp * multiplier)
        self.exp += gained
        self.completed_quests += 1
        self.rank = self.rank_for_exp(self.exp)
        self.save(update_fields=["exp", "completed_quests", "rank"])

    @property
    def can_accept_more_quests(self) -> bool:
        """
        Enforce quest limits:
        - non-premium users can complete only 3 quests in total
        - premium users have no quest limit
        """
        if self.is_premium:
            return True
        return self.completed_quests < 3

