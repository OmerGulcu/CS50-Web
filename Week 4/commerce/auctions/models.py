from distutils.command.upload import upload
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    price = models.PositiveIntegerField()
    image = models.CharField(max_length=2048, blank=True)
    categories = [("toys", "Toys"), ("electronics", "Electronics"), ("home", "Home"), ("fashion", "Fashion")]
    category = models.CharField(choices=categories, max_length=64, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    active = models.BooleanField(default=True)

class Bid(models.Model):
    amount = models.PositiveIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)

class Watching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchings")