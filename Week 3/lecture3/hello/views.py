from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def omer(request):
    return HttpResponse("Hello, Ömer!")

def deniz(request):
    return HttpResponse("Hello, Deniz and Sade!")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })