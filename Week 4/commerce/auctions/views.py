from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm

from .models import Listing, User

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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
                starting_bid = listing_form.cleaned_data["starting_bid"]
                image = listing_form.cleaned_data["image"]
                creator = request.user

                # Save as a listing
                listing = Listing(name = name, description = description, starting_bid = starting_bid, image = image, creator = creator)
                listing.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/new_listing.html", {"form": listing_form})

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ("name", "description", "starting_bid", "image")
        labels = {
            "image": "Image (url):"
        }

def view_listing(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, "auctions/view_listing.html", {
        "listing": listing
    })