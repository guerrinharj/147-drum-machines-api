from django.urls import path
from .views import KitDetailView

urlpatterns = [
    path("kits/<str:lookup>/", KitDetailView.as_view(), name="kit-detail"),
]