from django.urls import path
from .views import KitListView, KitDetailView

urlpatterns = [
    path("kits/", KitListView.as_view(), name="kit-list"),
    path("kits/<str:lookup>/", KitDetailView.as_view(), name="kit-detail"),
]