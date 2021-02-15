import re

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

import random

from . import util

class NewEntryForm(forms.Form):
    NewEntry = forms.CharField(label="New Entry")
    # NewEntryContent = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, entry):
    
    # entry = re.sub(r'?q=', '', entry)
    content = util.get_entry(entry)

    if content == None:
        return render(request, "encyclopedia/errorPage.html")

    else:
        return render(request, "encyclopedia/entries.html", {
            "content": content
    })


def add(request):
    if request.method == "POST":
        formEntry = NewEntryForm(request.POST)
        if formEntry.is_valid():
            NewEntryN = formEntry.cleaned_data["NewEntry"]
            Content = str(request.POST["content_data"])
            addressMd = f"entries/{NewEntryN}.md"
            try:
                with open(addressMd, 'x') as newEntryMd:
                    for line in Content.splitlines():
                        newEntryMd.write(line)
            except:
                return render(request, "encyclopedia/errorPage.html")
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "NewEntry": formEntry,
            })

    
    return render(request, "encyclopedia/newEntry.html", {
        "NewEntry": NewEntryForm()
    })



def editEntry(request):
    if request.method =="GET":
        print("GEEEET")
        global urlAddress
        global content
        global matchRe
        addressReferer = request.META['HTTP_REFERER']
        pattern = "http://127.0.0.1:8000/"
        replace = ""
        matchRe = str(re.sub(pattern, replace, addressReferer))
        urlAddress = f"entries/{matchRe}.md"
        content = util.get_entry(matchRe)
        return render(request, "encyclopedia/editEntry.html", {
            "content": content,
            # "urlAddress": urlAddress,
            # "matchRe": matchRe
        })
    
    if request.method == "POST":
        ContentAppend = str(request.POST["content_data"])
        # print(dir(request))
        # print(ContentAppend)
        # urlAddress = str(request.POST["urlAddress"])
        # matchRe = str(request.POST["matchRe"])
        # print(ContentAppend)
        # print(urlAddress)
        # print(matchRe)
        try:
            with open(urlAddress, 'a') as editEntryMd:
                for line in ContentAppend.splitlines():
                    editEntryMd.write(line)
                    editEntryMd.write("\n")
            content = util.get_entry(matchRe)
            matchRe = "/" + matchRe
            return redirect(matchRe)
        except:
            return render(request, "encyclopedia/errorPage.html")

def RandomPage(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)
    return redirect("encyclopedia:entries", entry=selected_page)
