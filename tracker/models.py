from django.conf import settings
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator


class Expense(models.Model):

    class Category(models.TextChoices):  
        FOOD = "Food"
        TRANSPORT ="Transport"
        BILLS = "Bills"
        SHOPPING = "Shopping"
        ENTERTAINMENT = "Entertainment"
        OTHER = "Other"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=Category.choices,default=Category.OTHER)
    store = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField(default=timezone.now)
    description = models.TextField(max_length=150, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)