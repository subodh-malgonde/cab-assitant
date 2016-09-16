from datetime import datetime
from pytz import timezone
import requests

FB_VERIFY_TOKEN = 'my_uber_assistant' # you can set this to any string. Need to add this same string in Messenger settings. Refer README.md for more details

FB_PAGE_ACCESS_TOKEN = '<your token>'

# Your own messenger recipient ID.
MESSENGER_RECIPIENT_ID = "<your recipient id>"

UBER_SERVER_TOKEN = "<your server token>"

UBER_ACCESS_TOKEN = "<your access token>"

HEADERS = {
    "Authorization": "Bearer %s" % UBER_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

office = {
    "latitude": 28.4659931,
    "longitude": 77.0810147
}

home = {
    "latitude": 28.4495637,
    "longitude": 77.0957114
}

ACCEPTABLE_SURGE_MULTIPLIER = 1.5


def get_pool_product_id(origin):
    url = "https://api.uber.com/v1/products?latitude=%s&longitude=%s&server_token=%s" %\
          (origin["latitude"], origin["longitude"], UBER_SERVER_TOKEN)
    response = requests.get(url)
    pool_product_id = None
    if response and response.status_code == 200:
        json_response = response.json()
        for product in json_response["products"]:
            if product["shared"]:
                pool_product_id = product["product_id"]
                break
    return pool_product_id


def get_fare_estimate(origin, destination, product_id):
    url = "https://api.uber.com/v1/requests/estimate"
    params = {
        "start_latitude": origin["latitude"],
        "start_longitude": origin["longitude"],
        "end_latitude": destination["latitude"],
        "end_longitude": destination["longitude"],
        "seat_count": 1,
        "product_id": product_id
    }
    response = requests.post(url, json=params, headers=HEADERS)

    if response and response.status_code == 200:
        json_response = response.json()
        if "price" in json_response:
            return {
                "fare_id": json_response["price"]["fare_id"],
                "surge_multiplier": json_response["price"]["surge_multiplier"]
            }
    return None


def book_trip(from_home=False):
    if from_home:
        origin = home
        destination = office
    else:
        origin = office
        destination = home
    product_id = get_pool_product_id(origin)
    if product_id:
        estimate = get_fare_estimate(origin, destination, product_id)
        if estimate:
            if estimate["surge_multiplier"] < ACCEPTABLE_SURGE_MULTIPLIER:
                url = "https://api.uber.com/v1/requests"
                params = {
                    "product_id": product_id,
                    "fare_id": estimate["fare_id"],
                    "end_latitude": destination["latitude"],
                    "end_longitude": destination["longitude"],
                    "start_latitude": origin["latitude"],
                    "start_longitude": origin["longitude"],
                    "seat_count": 1
                }
                response = requests.post(url, json=params, headers=HEADERS)
                if response.status_code == 202:
                    message = "Ride booked"
                else:
                    message = "Failed to book ride. Status code %d" % response.status_code
            else:
                message = "Surge of %sx" % estimate["surge_multiplier"]
        else:
            message = "Unable to get estimates"
    else:
        message = "Pool not available"
    return message


def send_message(text, recipient_id):
    if recipient_id == MESSENGER_RECIPIENT_ID:
        text = text.strip().lower()
        if text == "book":
            now = datetime.now(timezone("UTC")).astimezone(timezone("Asia/Kolkata"))
            if 8 <= now.hour <= 11:
                response = book_trip(True)
            elif 17 <= now.hour <= 23:
                response = book_trip(False)
            else:
                response = "You are out of your usual travel time. Use the Uber app to book"
        elif text == "hi":
            response = "Hi, I am here to help you book your Uber rides. Say 'book' to book a cab"
        else:
            response = "Did not understand. Say 'hi' to know more"
    else:
        response = "I only have 1 master and obey only his commands"
    message = {'recipient': {'id': recipient_id}, 'message': {'text': response}}
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % FB_PAGE_ACCESS_TOKEN
    json_response = requests.post(url, json=message)
    return json_response.json()


def handle(event, context):
    if "params" in event and "querystring" in event["params"]:
        query_params = event["params"]["querystring"]
        if "hub.mode" in query_params:
            if query_params["hub.mode"] == "subscribe" and query_params["hub.verify_token"] == FB_VERIFY_TOKEN:
                return int(query_params["hub.challenge"])
            else:
                return "Error in verifying code"
        else:
            return "invalid request"
    elif "object" in event:
        if event["object"] == "page":
            response = {"status": "not ok"}
            for entry in event['entry']:
                for message in entry['messaging']:
                    if 'message' in message:
                        incoming_message = message['message']
                        response_text = incoming_message['text']
                        response = send_message(response_text, message['sender']['id'])
            return "OK"
    return event