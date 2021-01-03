import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response 
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Tweets
from .forms import TweetForm
from .serializers import TweetSerializer

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    data = request.POST
    serializer = TweetSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status = 201)
    return Response({}, status = 400)

@api_view(['GET'])
def tweet_list_view(request,*args,**kwargs):
    qs = Tweets.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args,**kwargs):
    qs = Tweets.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args,**kwargs):
    qs = Tweets.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user = request.user)
    if not qs.exists():
        return Response({"message": "You can not delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Successfully Deleted"}, status=200)





def tweet_create_view_pure_django(request, *args, **kwargs):
    print("ajax", request.is_ajax())
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None 
    print(next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view_pure_django(request,*args,**kwargs):
    qs = Tweets.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweet_list 
    }
    return JsonResponse(data)
def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):

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