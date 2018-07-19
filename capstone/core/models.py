
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from datainput.models import Barangay


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True, blank=True)

    USER_TYPES = (
        ('Barangay Nutrition Scholar', 'Barangay Nutrition Scholar'),
        ('Nutritionist', 'Nutritionist'),
        ('Nutrition Program Coordinator', 'Nutrition Program Coordinator')
    )

    user_type = models.CharField(max_length=40, choices=USER_TYPES)

    def __str__(self):
        return self.user.username

    @property
    def get_name(self):

        return '%s %s' % (self.user.first_name, self.user.last_name)


class Notification(models.Model):

    date = models.DateTimeField(default=datetime.now)
    profile_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_to')
    profile_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_from')
    message = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message + " for " + self.profile_to.user.username