from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=128, verbose_name='Name')
    capacity = models.IntegerField(verbose_name='Capacity')
    projector = models.BooleanField(verbose_name='Projector availability')


class Reservation(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
