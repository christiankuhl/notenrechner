from django.urls import path
from notenrechner import views

app_name = 'notenrechner'
urlpatterns = [
        path('', views.index, name="index"),
        path("klassen", views.klassen, name="klassen"),
        path("overview", views.overview, name="overview"),
        path("klausur", views.klausur, name="klausur"),
    ]
