import requests
import paho.mqtt.subscribe as subscribe
import http.client, urllib
import json

def add_items_to_cart(token, items):
    # Conducts a PUT request using the 30 minute access token and the item information
    url = 'https://api.kroger.com/v1/cart/add'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    data = {'items': [items]}
    response = requests.put(url, headers=headers, data=json.dumps(data))
    #submits a PUT request to add the item to the cart and returns the status code to determine if the operation was a success
    return response.status_code


def get_mqtt_token():
    msg = subscribe.simple("kroger/access_token", hostname="192.168.1.215")
    decoded_string = msg.payload.decode("utf-8")
    return decoded_string

############################################################
#               Get Product Function                       #
############################################################
def get_product(upc, token):
    # Takes the upc of the scanned product and the access token in order to run the GET request
    search = {
        "productId": upc,
        "upc": upc,
        # In order to get prices, you have to include the filter.locationId parameter in the request. 
        "filter.locationId": "01100644"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    product = requests.get(f"https://api.kroger.com/v1/products/{upc}", headers=headers, params=search)
    json = product.json()
    # Returns the JSON for the product information which is broken out by the get_product_info function
    return json


############################################################
#               Get Product Information                    #
############################################################
def get_product_info(product):
    # product is the json returning from the get product function
    # Isolates the data key
    newest = product['data']
    # Declares the product description
    try:
        description = newest['description']
    except:
        description = "No Description Found"
    try:
        brand = newest['brand']
    except:
        brand = "No Brand Found"
    try:
        category = newest['categories'][0]
    except:
        category = "No Category Found"
    try:
        productId = newest['productId']
    except:
        productId = "No UPC Found"
    # Declares the product size
    try:
        size = newest['items'][0]['size']
    except:
        size = "No Size Found"
    try:
        price = newest['items'][0]['price']['regular']
    except:
        price = "No price found"
    try:
        promo_price = newest['items'][0]['price']['promo']
    except:
        promo_price = 0
    # Locates the images asssociated with the product
    try:
        images = newest['images']
        imgurl = ""
        # Locates the url for the 'large' size image of the product.
        for p in images:
            if p['perspective'] == "front":
                sizes = p['sizes']
                for i in sizes:
                    if i['size'] == "thumbnail":
                        imgurl = i['url']
    except:
        images = 'No images found'
    try:
        price_regular = newest['items'][0]['price']['regular']
    except:
        price_regular = 0
    try:
        price_promo = newest['items'][0]['price']['promo']
    except:
        price_promo = 0
    return description, size, imgurl, brand, category, productId, price_regular, price_promo




# Replace with your Home Assistant URL and Long-Lived Access Token
HA_URL = "http://192.168.1.227:8123"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhZTA1OTQ2YjAxNTg0Zjk4YjFmZDY5N2UzNzgxNGNhMiIsImlhdCI6MTc2NTEzMjI0MywiZXhwIjoyMDgwNDkyMjQzfQ.UHheBNFpVk8cC0WOqoMBzy18XTHPi4oC5QD5_rehDSQ"
def send_ha_notification(message, title="Scanner Notification", target=None):
    """Sends a notification to Home Assistant."""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "message": message,
        "title": title,
    }
    
    if target:
        payload["target"] = target # e.g., ["notify.mobile_app_your_device_name"]

    response = requests.post(f"{HA_URL}/api/services/notify/persistent_notification", headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Error sending notification: {response.status_code} - {response.text}")
