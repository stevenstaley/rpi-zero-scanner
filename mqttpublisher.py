import time
import paho.mqtt.client as mqtt
from functions import get_valid_access_token

MQTT_HOST = '192.168.1.x'
MQTT_TOPIC_ACCESS = "homeassistant/kroger/access_token"
MQTT_TOPIC_REFRESH = "homeassistant/kroger/refresh_token"

def publish_tokens(client, tokens):
    client.publish(MQTT_TOPIC_ACCESS, str(tokens['access_token']), retain=True)
    client.publish(MQTT_TOPIC_REFRESH, str(tokens['refresh_token']), retain=True)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_HOST)
client.loop_start()

while True:
    try:
        tokens = get_valid_access_token()
        print(tokens['access_token'])
        print(tokens['refresh_token'])
        publish_tokens(client, tokens)
    except Exception as e:
        print(f'Token refresh error: {e}')
    time.sleep(60)
