from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("displaysearchresults", views.display_search_results, name = "display_search_results"),
    path("createnewentry", views.create_new_entry, name = "create_new_entry"),
    path("randompage", views.get_random_page, name = "get_random_page"),
    path("<str:title>", views.display_entry, name = "display_entry"),
    path("edit/<str:title>", views.edit_entry, name = "edit_entry")
]
