from distutils.command.upload import upload
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.PositiveIntegerField()
    image = models.CharField(max_length=2048, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    active = models.BooleanField(default=True)

class Bid(models.Model):
    amount = models.PositiveIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
