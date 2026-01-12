from django.db import models

from user.models import User
from vehicle.models import Vehicle


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    # id otomatis dibuat Django sebagai AutoField (integer)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    class Meta:
        db_table = "reservations"

        indexes = [
            models.Index(fields=['vehicle', 'start_date', 'end_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.name} ({self.start_date} to {self.end_date})"

    def is_active(self):
        """Return True if the reservation is ongoing or in the future."""
        from datetime import date
        return self.end_date >= date.today()
