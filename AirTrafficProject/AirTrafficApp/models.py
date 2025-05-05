from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class ArchiveGroup(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)


class Items(models.Model):
    choices1 = [
        ('Fixed Wing', 'Fixed Wing'),
        ('Helicopter', 'Helicopter')
    ]

    choices2 = [
        ('Arrival', 'Arrival'),
        ('Departure', 'Departure'),
        ('Enroute', 'Enroute')
    ]

    choices3 = [
        ('Commercial', 'Commercial (Domestic)'),
        ('Private', 'Private'),
        ('Med_evac', 'Med Evac'),
        ('Util/Maint', 'Utility/Maintenance'),
        ('Government', 'Government'),
        ('Military', 'Military'),
    ]

    choices4 = [
        ('Delayed', 'Delayed'),
        ('On Time', 'On Time'),
        ('N/A', 'N/A (For Enroute)'),
    ]

    call_sign = models.CharField(max_length=20)
    aircraft_type = models.CharField(max_length=20)
    detail = models.CharField(max_length=20, choices=choices1, default='fixed_wing')
    origin = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    action = models.CharField(max_length=20, choices=choices2, default='arrival')
    time = models.CharField(max_length=20)
    timeliness = models.CharField(max_length=20, choices=choices4, default='on_time')
    remarks = models.CharField(max_length=30, choices=choices3, default='commercial')
    date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    archive_group = models.ForeignKey(ArchiveGroup, on_delete=models.SET_NULL, null=True, blank=True)



    
