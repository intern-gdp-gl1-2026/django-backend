from django.db import models

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    plate_number = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=30)
    daily_rate = models.IntegerField()
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=50)

    class Meta:
        db_table = "vehicles"

    def __str__(self):
        return self.name