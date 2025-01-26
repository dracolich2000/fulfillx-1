from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class StaffUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('User', 'User'),
        ('Vendor', 'Vendor')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='staffuser_set',  # Custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='staffuser_set',  # Custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )