from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweets
from .forms import TweetForm

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={})

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view(request,*args,**kwargs):
    qs = Tweets.objects.all()
    tweet_list = [{"id":x.id, "content":x.content} for x in qs]
    data = {
        "isUser": False,
        "response": tweet_list 
    }
    return JsonResponse(data)
def tweet_detail_view(request, tweet_id, *args, **kwargs):

    data = {
        "id": tweet_id
    }
    status = 200
    try:
        obj = Tweets.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)