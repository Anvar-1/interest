from django.urls import path
from .views import UserProfileDetailView

urlpatterns = [
    path('detail/', UserProfileDetailView.as_view(), name='user-profile-detail'),
]