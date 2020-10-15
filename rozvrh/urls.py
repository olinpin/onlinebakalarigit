from django.urls import path

from . import views

app_name = "rozvrh"
urlpatterns = [
    path("", views.index, name="index"),
    #path("<str:name>", views.greet, name="greet"),
    path('privacy', views.PrivacyPolicy, name="privacy"),
    path('form', views.rozvrhAdd, name="rozvrhAdd")
]