from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm

from .models import User, Listing, Bid, Comment, Watching

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings, "header": "Active Listings"
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

@login_required(login_url='login')
def new_listing(request):
    if request.method == "GET":
        listing_form = ListingForm()
    else:
        listing_form = ListingForm(request.POST)
        if request.user.is_authenticated:
            if listing_form.is_valid():

                # Get cleaned data
                name = listing_form.cleaned_data["name"]
                description = listing_form.cleaned_data["description"]
                price = listing_form.cleaned_data["price"]
                image = listing_form.cleaned_data["image"]
                category = listing_form.cleaned_data["category"]
                creator = request.user

                # Save as a listing
                listing = Listing(name = name, description = description, price = price, image = image, category = category, creator = creator)
                listing.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/new_listing.html", {"forma": listing_form})

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ("name", "description", "price", "image", "category")
        labels = {
            "image": "Image (url):"
        }

def view_listing(request, id):
    user = request.user
    listing = Listing.objects.get(id=id)
    error = False

    try:
        Watching.objects.get(user = user, listing = listing)
        watched = True
    except Watching.DoesNotExist:
        watched = False
    except TypeError:
        watched = False

    if request.method == "POST":
        if request.POST["post"] == "Place Bid":
            form = BidForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data["amount"]
                if amount > listing.price:
                    bid = Bid(amount=amount, listing=listing, user=user)
                    bid.save()
                    listing.price = bid.amount
                    listing.winner = bid.user
                    listing.save()

                    # Getting the highest bid in a listing

                    # bids = listing.bids.all()
                    # for bid in bids:
                    #     if bid.amount > listing.price:
                    #         listing.price = bid.amount
                    #         listing.winner = bid.user
                    #         listing.save()

                else:
                    message = "Your bid must be higher than the current price."
                    error = True
        elif request.POST["post"] in ["In Watchlist", "Add to Watchlist"]:
            if not watched:
                watching = Watching(user = user, listing = listing)
                watching.save()
                watched = True
            else:
                Watching.objects.get(user = user, listing = listing).delete()
                watched = False

    if not error:
        return render(request, "auctions/view_listing.html", {
       "listing": listing, "watched": watched, "bid_form": BidForm()
        })
    else:
        return render(request, "auctions/view_listing.html", {
       "listing": listing, "watched": watched, "bid_form": BidForm(), "message": message
        })
    
class BidForm(forms.Form):
    amount = forms.IntegerField(label="")

@login_required(login_url="login")
def watchlist(request):
    watchings = request.user.watchings.all()
    listings = []
    for watching in watchings:
        listings.append(watching.listing)
    return render(request, "auctions/index.html", {
        "listings": listings, "header": "Watchlist"
    })

category_list = ["toys", "electronics", "home", "fashion"]

def category(request, category):
    if category not in category_list:
        return HttpResponse("Page not found.")
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings, "header": category.capitalize()
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": category_list
    })