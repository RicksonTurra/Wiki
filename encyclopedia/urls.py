from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("edit", views.editEntry, name="editEntry"),
    path("random", views.RandomPage, name="random_page"),
    path("<str:entry>", views.entries, name="entries"),
]
