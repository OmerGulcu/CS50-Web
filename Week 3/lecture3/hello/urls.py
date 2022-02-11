from hello.views import index
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("omer", views.omer, name = "omer"),
    path("deniz", views.deniz, name = "deniz"),
    path("<str:name>", views.greet, name = "greet")
]