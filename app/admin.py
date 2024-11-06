from django.contrib import admin
from .models import User_DB,admin_add_auction_items,Bid

admin.site.register(User_DB)
admin.site.register(admin_add_auction_items)
admin.site.register(Bid)
