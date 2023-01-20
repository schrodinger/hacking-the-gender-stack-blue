from django.urls import path

from . import views

urlpatterns = [path("", views.SimilarityMap.as_view())]
