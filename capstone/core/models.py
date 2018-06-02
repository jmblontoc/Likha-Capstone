from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from datainput.models import Barangay


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True, blank=True)

    USER_TYPES = (
        ('Barangay Nutrition Scholar', 'Barangay Nutrition Scholar'),
        ('Nutritionist', 'Nutritionist'),
        ('Nutrition Program Coordinator', 'Nutrition Program Coordinator')
    )

    user_type = models.CharField(max_length=40, choices=USER_TYPES)

    def __str__(self):
        return self.user.username


class Notification(models.Model):

    date = models.DateTimeField(default=datetime.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.message + " for " + self.profile.user.username