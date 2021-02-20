from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class User(AbstractUser):
    pass


class Auction(models.Model):
    name = models.CharField(max_length=64)
    photo = models.CharField(max_length=200, default=None, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()
    dateInsert = models.DateTimeField()
    dateFinish = models.DateTimeField(default=None, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'auction'], name='Watchlist Item')
        ]


class Bid(models.Model):
    price = models.FloatField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


