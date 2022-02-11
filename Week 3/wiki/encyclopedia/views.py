from logging import PlaceHolder
from django import forms
from django.forms.fields import CharField
from django.forms.forms import Form
from django.shortcuts import render
from django.http import HttpResponse
import markdown2
import random

from . import util
import encyclopedia

class search_form(forms.Form):
    title = forms.CharField(label = "", widget = forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class entry_form(forms.Form):
    title = forms.CharField(label = "Entry Title")
    content = forms.CharField(label = "Entry Content", widget = forms.Textarea(attrs={'value': 'hello'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": search_form()
    })

def display_entry(request, title):
    entry = util.get_entry(title)
    if entry:
        if entry.split()[0] == "#":
            title = entry.split()[1]
        else:
            title = entry.split()[0]
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry), "title": title, "form": search_form()
        })
    else:
        return HttpResponse("Page not found!!!")
        

def display_search_results(request):
    if request.method == "POST":
        form = search_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].lower()
            title_valid = False
            for entry in util.list_entries():
                if title == entry.lower():
                    title_valid = True
            if title_valid:
                return display_entry(request, title)
            else:
                possible_entries = []
                for entry in util.list_entries():
                    if title in entry.lower():
                        possible_entries.append(entry)
                return render(request, "encyclopedia/results.html", {
                    "entries": possible_entries, "form": search_form()
                })
    else:
        return HttpResponse("Page not found!!!")

def create_new_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html", {
            "form": search_form(), "entry_form": entry_form()
        })
    else:
        create_form = entry_form(request.POST)
        if create_form.is_valid():
            title = create_form.cleaned_data["title"]
            content = create_form.cleaned_data["content"]
            title_exists = False
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    title_exists = True
            if title == "admin":
                return HttpResponse("Can't add a new entry titled 'admin'.")
            elif not title_exists:
                util.save_entry(title, content)
                return display_entry(request, title)
            else:
                return HttpResponse("Entry already exists.")

def edit_entry(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title, "form": search_form(), "content": util.get_entry(title)
        })
    elif request.method == "POST":
        edit_form = request.POST
        content = edit_form["content"]
        util.save_entry(title, content)
        return display_entry(request, title)

def get_random_page(request):
    title = random.choice(util.list_entries())
    return display_entry(request, title)
