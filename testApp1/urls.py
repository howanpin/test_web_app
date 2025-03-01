from django.urls import path

from . import views

urlpatterns = [
    path("", views.one_rm_max, name="one_rm_max"),
    path("hps_program/", views.hps_program, name="hps_program"),
]