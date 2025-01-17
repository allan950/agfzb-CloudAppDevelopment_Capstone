from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
# from .restapis import related methods
from django.urls import reverse
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
            return redirect("djangoapp:index")
        else:
            return redirect('djangoapp/index')
    else:
        return redirect('djangoapp/index')


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
        print(dealerships)
        context['dealerships'] = dealerships

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/get-reviews.json'
        dealer_url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/get-all-dealerships.json'
        
        dealerId = {"id": str(dealer_id)}
        dealer = get_dealer_by_id(dealer_url, dealerId=dealerId)
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealerId)
        context['reviews'] = reviews
        context['dealer'] = dealer

        context['dealer_id'] = dealer_id
        print(dealer[0])

        return render(request, 'djangoapp/dealer_details.html', context)

        #return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details', args=(dealer_id,)))

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    cars = CarModel.objects.filter(dealer_id=dealer_id)
    username = request.user
    if request.method == "GET":
        dealer_url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/get-all-dealerships.json'
        dealerId = {"id": str(dealer_id)}

        dealer = get_dealer_by_id(dealer_url, dealerId=dealerId)
        context['cars'] = cars
        context['dealerName'] = dealer[0].full_name
        context['dealer_id'] = dealer_id
        print(cars)

        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/get-reviews.json'
        dealerId = {"id": str(dealer_id)}
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealerId)
        CHECKBOX_MAPPING = {'on':True,
                    'off':False,}
        
        for i in reviews:
            print(i)

        review = dict()
        review["id"] = len(reviews) + 1
        review["name"] = str(username)
        review["dealership"] = dealer_id
        review["review"] = request.POST["review"]
        if request.POST["purchase"] == 'on':
            review["purchase"] = CHECKBOX_MAPPING.get(request.POST["purchase"])
        review["purchase_date"] = request.POST["purchase_date"]
        for car in cars:
            if car.id == int(request.POST["car"]):
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")
        #review["car_make"] = request.POST["car_make"]
        #review["car_model"] = request.POST["car_model"]
        #review["car_year"] = request.POST["car_year"]

        print(review)

        json_payload = dict()
        json_payload["review"] = review

        url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/9f382676-5b7e-4225-ae28-50d290bd7ba2/dealership/post-reviews'
        result = post_request(url, json_payload, dealer_id=dealer_id)

        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        #return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details', args=(dealer_id,)))
