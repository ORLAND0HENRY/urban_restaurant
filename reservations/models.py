from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Confirmation'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('SEATED', 'Seated'),
    ]

    # Change: null=True allows guests to book without an account initially
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
        null=True,
        blank=True
    )

    # Guest Info (Required if user is null)
    guest_name = models.CharField(max_length=100, blank=True, null=True)
    guest_phone = models.CharField(max_length=15, blank=True, null=True)

    date = models.DateField()
    time = models.TimeField()

    # Validation: Ensure they don't book for 0 or 100 people
    party_size = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    notes = models.TextField(blank=True, help_text="Allergies or special occasions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']
        # Prevent the same user from booking the exact same time twice
        unique_together = ['user', 'date', 'time']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        customer = self.user.username if self.user else self.guest_name
        return f"{customer} - {self.date} at {self.time} ({self.status})"