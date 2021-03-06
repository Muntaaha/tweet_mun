from django.contrib import admin
from django.urls import path
from tweets.views import home_view,tweet_list_view,tweet_create_view,tweet_detail_view,tweet_delete_view,tweet_action_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('tweets/', tweet_list_view),
    path('tweet_create/', tweet_create_view),
    path('api/tweets/<int:tweet_id>/delete', tweet_delete_view),
    path('api/tweets/action', tweet_action_view),
    path('tweet_detail/<str:tweet_id>/', tweet_detail_view),
]
