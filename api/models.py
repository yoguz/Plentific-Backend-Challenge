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


class Chart1(models.Model):
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    detached_avg = models.IntegerField()
    semidetached_avg = models.IntegerField()
    terraced_avg = models.IntegerField()
    flats_avg = models.IntegerField()


class Chart2(models.Model):
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    labels = models.CharField(max_length=200)
    values = models.CharField(max_length=200)
