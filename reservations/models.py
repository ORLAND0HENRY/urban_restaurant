from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Reservation(models.Model):
    """
    Model to track table reservations made by users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    party_size = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending Confirmation'),
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled'),
            ('SEATED', 'Seated'),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.date} at {self.time}"