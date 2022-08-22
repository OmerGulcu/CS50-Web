from distutils.command.upload import upload
from django.contrib.auth.models import AbstractUser
from django.db import models

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.PositiveIntegerField()
    image = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="listings")
    watchlist = models.BooleanField(default=False)

class Bid(models.Model):
    amount = models.PositiveIntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, related_name="bids")

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, related_name="comments")

class User(AbstractUser):
    pass
