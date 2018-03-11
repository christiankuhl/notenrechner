from django.urls import path
from notenrechner import views

app_name = 'notenrechner'
urlpatterns = [
        path('', views.index, name="index"),
        path("klassen", views.view_klassen, name="klassen"),
        path("overview", views.overview, name="overview"),
        path("klausur/<int:klausur_id>", views.view_klausur, name="klausur"),
        path("klausur/<int:klausur_id>/evaluate", views.klausur_evaluation, name="evaluate"),
        path("klausur/<int:klausur_id>/detail", views.klausur_detail, name="detail"),
        path("klausuren", views.view_klausuren, name="klausuren"),
        path("klasse/<int:klassen_id>", views.view_klasse, name="klasse"),
    ]
