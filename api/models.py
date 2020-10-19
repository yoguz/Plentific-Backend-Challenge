from django.db import models


class Postcode(models.Model):
    postcode = models.CharField(max_length=10, unique=True)


class Date(models.Model):
    date_str = models.CharField(max_length=10, unique=True)
    date = models.DateField()


class Transaction(models.Model):
    price = models.IntegerField()
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=1)
