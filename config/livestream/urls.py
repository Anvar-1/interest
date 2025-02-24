from django.urls import path
from .views import LiveStreamListCreateView, LiveStreamDetailView

urlpatterns = [
    path('live-streams/', LiveStreamListCreateView.as_view(), name='live-stream-list-create'),
    path('live-streams/<int:pk>/', LiveStreamDetailView.as_view(), name='live-stream-detail'),
]