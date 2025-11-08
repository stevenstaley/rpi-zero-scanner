from functions import add_items_to_cart, get_mqtt_token, send_pushover, get_product, get_product_info, send_ha_notification
import time

time.sleep(60)

send_ha_notification("Scanner ready")

while True:
    print("Waiting for input")
    upc = input()
    items = {
        "upc": upc,
        "quantity": 1          
    }
    while True:
        token = get_mqtt_token()
        status = add_items_to_cart(token, items)
        if status == 401:
            # send_pushover("Product not added.")        
            send_ha_notification("Product not added.")
            break
               
        elif status == 400:
            # User probably left it blank or UPC was not found
            # send_pushover("Product not added, UPC incorrect.")  
            send_ha_notification("Product not added, errors.")
            
            break
            
        elif status == 204:
            # Success
            # try:
            product = get_product(upc, token)
            # print(product)
            description, size, imgurl, brand, category, productId, price_regular, price_promo = get_product_info(product)
            # Standard message for adding something to the cart
            message = f"{description}, {size}, ${price_regular}, ${price_promo}" + " has been added to your cart"
            # send_pushover(message)
            send_ha_notification(message)
            # except:
                # print("Try again")
            break
    