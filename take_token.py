import json, requests
from password import passwd, phone

f = open('token.txt', 'w')

api_token = requests.get("https://api.vk.com/oauth/token?grant_type=password&client_id=2274003&scope=messages&client_secret=hHbZxrka2uZ6jB1inYsH&username={0}&password={1}".format(phone, passwd))
api_token = api_token.text
api_token = json.loads(api_token)
api_token = api_token["access_token"]

f.write(api_token)
