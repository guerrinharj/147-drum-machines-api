from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Kit
from .serializers import KitSerializer


class KitListView(ListAPIView):
    queryset = Kit.objects.all().order_by("name")
    serializer_class = KitSerializer


class KitDetailView(APIView):
    def get(self, request, lookup):
        if lookup.isdigit():
            kit = get_object_or_404(Kit, id=int(lookup))
        else:
            kit = get_object_or_404(Kit, slug=lookup)

        return Response(KitSerializer(kit).data)