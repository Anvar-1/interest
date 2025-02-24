from rest_framework import generics
from .models import LiveStream
from .serializers import LiveStreamSerializer
from rest_framework.permissions import IsAuthenticated


class LiveStreamListCreateView(generics.ListCreateAPIView):
    queryset = LiveStream.objects.all()
    serializer_class = LiveStreamSerializer
    permission_classes = [IsAuthenticated]

class LiveStreamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LiveStream.objects.all()
    serializer_class = LiveStreamSerializer
    permission_classes = [IsAuthenticated]
