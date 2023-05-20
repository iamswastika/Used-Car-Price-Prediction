from django.db import models

# Create your models here.

Owner_type = (
    ("0", "First"),
    ("1" , "Second"),
    ("2" , "Third"),
    ("3", "Fourth & Above"),
)

Transmission_type  = (
    ("0", "Manual"),
    ("1", "Automatic")
)

Fuel_type = (
    ("0", "CNG"),
    ("1", "Diesel"),
    ("2", "Petrol"),
    ("3", "LPG"),
    ("4", "Electric")
)


class PredictCarModel(models.Model):
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    kilometer_driven = models.FloatField(default=0)
    mileage = models.FloatField()
    engine = models.FloatField()
    owner_type = models.CharField(max_length=150, choices=Owner_type)
    transmission_type = models.CharField(max_length=150, choices=Transmission_type)
    fuel_type = models.CharField(max_length=150, choices=Fuel_type)
    power = models.FloatField()
    seat = models.FloatField(default=0)
    predicted_price1 = models.FloatField(null=True, blank=True)
    predicted_price2 = models.FloatField(null=True, blank=True)
    predicted_price3 = models.FloatField(null=True, blank=True)



    def __str__(self) -> str:
        return self.model

