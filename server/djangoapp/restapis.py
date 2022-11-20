import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    #kwargs = kwargs['kwargs']
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            kwargs = dict()
            kwargs["text"] = kwargs["text"]
            kwargs["version"] = kwargs["version"]
            kwargs["features"] = kwargs["features"]
            kwargs["return_analyzed_text"] = kwargs["return_analyzed_text"]
            
            response = requests.get(url, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key)
                                        params=kwargs)
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, **kwargs):
    result = []
    json_result = get_request(url, dealerId=kwargs)
    if json_result:
        dealers = json_result['result']
        for dealer in dealers:
            dealer_doc = dealer['doc']
            if dealer_doc["id"] == dealerId:
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                        id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                        short_name=dealer_doc["short_name"],
                                        st=dealer_doc["st"], zip=dealer_doc["zip"])
                result.append(dealer_obj)
    return result


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    result = []
    dealerId = 15
    json_data = get_request(url, dealerId=dealerId)
    if json_data:
        dealers = json_data['body']['data']['docs']
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = DealerReview(car_make = dealer_doc['car_make'],
                car_model = dealer_doc['car_model'],
                car_year = dealer_doc['car_year'],
                dealership = dealer_doc['dealership'],
                id = dealer_doc['id'],
                name = dealer_doc['name'],
                purchase = dealer_doc['purchase'],
                purchase_date = dealer_doc['purchase_date'],
                review = dealer_doc['review'],
                sentiment = analyze_review_sentiments(dealer_doc['review']))
            result.append(dealer_obj)
    return result



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    sentiment = get_request(url, dealerreview)
    return sentiment


