from django.urls import path

from . import views

urlpatterns = [path("", views.Proprieties.as_view())]
