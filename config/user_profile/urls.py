from django.urls import path
from .views import UserProfileDetailView, SubscribeView, SubscriberListView, UnsubscribeView

urlpatterns = [
    path('detail/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('subscribe/<int:user_id>/', SubscribeView.as_view(), name='subscribe'),
    path('subscribers/', SubscriberListView.as_view(), name='subscriber-list'),
    path('unsubscribe/<int:user_id>/', UnsubscribeView.as_view(), name='unsubscribe'),
]