from django.db import models


# Create your models here.
class UserData(models.Model):
    Email = models.CharField(max_length=50, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    EmployeeNumber = models.CharField(max_length=50, null=True, blank=True)
    Department = models.CharField(max_length=50, null=True, blank=True)
    City = models.CharField(max_length=50, null=True, blank=None)
