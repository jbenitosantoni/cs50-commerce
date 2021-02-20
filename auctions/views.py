from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import *


def index(request):
    auctions = Auction.objects.filter(dateFinish=None)

    return render(request, "auctions/index.html", {
        "auctions": auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def new_listing(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/new_listing.html", {
            "categories": categories
        })
    if request.method == "POST":
        photo = None
        category = None
        if request.POST["photo"]:
            image = request.POST["photo"]
        if request.POST["category"]:
            category = request.POST["photo"]
        auction = Auction(name=request.POST["name"], description=request.POST["description"],
                          initialPrice=request.POST["price"], photo=photo, user=User.objects.get(pk=request.user.id),
                          category=category, dateInsert=datetime.datetime.now())
        auction.save()
        return index(request)


def list_auction(request, auction, error=None):
    auction = Auction.objects.get(pk=auction)
    user = User.objects.get(pk=request.user.id)
    last_bid = util.get_last_bid(auction)
    try:
        comments = Comment.objects.filter(auction=auction)
    except:
        comments = None
    try:
        watchlist = WatchList.objects.get(auction_id=auction.id, user_id=user.id)
    except:
        watchlist = None
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "watchlist": watchlist,
        "last_bid": last_bid,
        "error": error,
        "comments": comments
    })


def add_watchlist(request, auction):
    auction = Auction.objects.get(pk=auction)
    user = User.objects.get(pk=request.user.id)
    WatchList(auction=auction, user=user).save()
    return list_auction(request, auction.id)


def remove_watchlist(request, auction):
    auction = Auction.objects.get(pk=auction)
    user = User.objects.get(pk=request.user.id)
    WatchList.delete(WatchList.objects.get(user=user, auction=auction))
    return list_auction(request, auction.id)


def new_vid(request, auction):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction)
        user = User.objects.get(pk=request.user.id)
        last_bid = util.get_last_bid(auction)
        if float(request.POST["price"]) > last_bid:
            Bid(auction=auction, user=user, price=request.POST["price"]).save()
            error = None
        else:
            error = "Vid must be greater than current price"
        return list_auction(request, auction, error)


def close(request, auction):
    if not request.user.is_authenticated:
        return list_auction(request, auction, "You must be logged")
    auction_object = Auction.objects.get(pk=auction)
    if auction_object.user_id == request.user.id:
        Auction.objects.filter(pk=auction).update(dateFinish=datetime.datetime.now())
        return list_auction(request, auction)


def comment(request, auction):
    if not request.user.is_authenticated:
        return list_auction(request, auction, "You must be logged")
    user = User.objects.get(pk=request.user.id)
    auction_object = Auction.objects.get(pk=auction)
    Comment(comment=request.POST["comment"], auction=auction_object, user=user).save()
    return list_auction(request, auction)