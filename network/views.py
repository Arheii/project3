import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Tweet


class NewTweet(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': "form-control", 'placeholder': "What you want say to the word?"}),
        }


def index(request):
    if request.method == "POST":
        form = NewTweet(request.POST)
        # if new form for tweet fill corectly -> save to db
        if form.is_valid():
            Tweet.objects.create(owner=request.user, body=form.cleaned_data['body'])
            # load page with new tweet
            return HttpResponseRedirect(reverse("tweets:index"))
    else:
        form = NewTweet()

    tweets = Tweet.objects.all()
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    tweets_on_page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "form": form,
            "title": "All tweets:",
            "userpage": None,
            "tweets_page": tweets_on_page
        })


def user_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Disable form if it's page other user
    if user != request.user:
        form = None

    # Enable form and POST query if it's yourself page
    elif request.method == "POST":
        form = NewTweet(request.POST)
        # if new form for lot fill corectly -> save to db
        if form.is_valid():
            Tweet.objects.create(owner=request.user, body=form.cleaned_data['body'])
            # load page with new tweet
            return HttpResponseRedirect(reverse("tweets:index", args=(user_id)))
    else:
        form = NewTweet()

    tweets = Tweet.objects.filter(owner=user_id)
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    tweets_on_page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "form": form,
            "title": f"{user} tweets:",
            "userpage": user,
            "tweets_page": tweets_on_page
        })


def following_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Disable newtweet form
    form = None

    tweets = Tweet.objects.filter(owner__in=user.folowing.all())
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    tweets_on_page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "form": form,
            "title": f"{user} following tweets:",
            "userpage": user,
            "tweets_page": tweets_on_page
        })


@login_required
def follow_or_unfollow(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if user != request.user:

        # Unfollow user_id from current loggin user
        if user in request.user.folowing.all():
            request.user.folowing.remove(user)
        # Follow
        else:
            request.user.folowing.add(user)

    return HttpResponseRedirect(reverse("tweets:user", args=(user_id)))


@login_required
def like_or_dislike(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    # dislike
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    # like
    else:
        tweet.likes.add(request.user)

    return HttpResponse(status=204)


@login_required
def edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    # User try edit not your tweet
    if request.user != tweet.owner:
        return HttpResponse(status=406)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(f"\ndata: {data}")
        if data.get("text") is not None:
            tweet.body = data["text"]
        else:
            JsonResponse({"new_text": tweet.body}, status=201)

        try:
            tweet.save()
        except:
            return JsonResponse({'error': 'incorrect data in text field'}, status=422)

    print(f"\nNew tweet text {tweet.body}")
    return JsonResponse({"new_text": tweet.body}, status=201)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("tweets:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("tweets:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("tweets:index"))
    else:
        return render(request, "network/register.html")
