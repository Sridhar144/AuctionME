from django.db import models

class User_DB(models.Model):
    name = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=16)
    age = models.IntegerField()
    tokens = models.IntegerField(default=100)

    def __str__(self):
        return self.name

class admin_add_auction_items(models.Model):
    item_name = models.CharField(max_length=256)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_price = models.IntegerField()

    def __str__(self):
        return self.item_name


class Bid(models.Model):
    user = models.ForeignKey(User_DB, on_delete=models.CASCADE)
    auction_item = models.ForeignKey(admin_add_auction_items, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

