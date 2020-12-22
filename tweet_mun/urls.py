from django.contrib import admin
from django.urls import path
from tweets.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('tweet_list/', tweet_list_view),
    path('tweet_detail/<str:tweet_id>/', tweet_detail_view),
]
