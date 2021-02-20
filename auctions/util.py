from .models import *


def get_last_bid(auction):
    bids = Bid.objects.filter(auction=auction).order_by('-price').first()
    if bids is None:
        bids = Auction.objects.get(id=auction.id)
    else:
        bids = bids
    return bids
