from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, get_request, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request): 
    context = {}
    print(User.objects.all())
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pwd']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:login")
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        existing_user = False
        try:
            User.objects.get(username=username)
            existing_user = True
        except:
            logger.error("New user!")
        
        if not existing_user:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['user_warn_msg'] = "Username has already been picked!"
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/get-all-dealerships.json'
        
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

        return HttpResponse(dealer_names)
        #return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/get-reviews.json'
        #reviews = get_dealer_reviews_from_cf(url)
        dealerId = {"id": str(dealer_id)}
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealerId)
        context['reviews'] = reviews
        return HttpResponse(reviews)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pwd']

        user = authenticate(username=username, password=password)
        print(user)
        if user:
            review = dict()
            review["id"] = request.POST["id"]
            review["name"] = request.POST["name"]
            review["dealership"] = request.POST["dealership"]
            review["review"] = request.POST["review"]
            review["purchase"] = request.POST["purchase"]
            review["purchase_date"] = request.POST["purchase_date"]
            review["car_make"] = request.POST["car_make"]
            review["car_model"] = request.POST["car_model"]
            review["car_year"] = request.POST["car_year"]

            json_payload = dict()
            json_payload["review"] = review

            url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/post-reviews'
            result = post_request(url, json_payload, dealer_id=dealer_id)

            return HttpResponse(result)