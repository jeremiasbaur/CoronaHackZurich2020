# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
# from msrest.authentication import CognitiveServicesCredentials
# import os

# region = "whatever123." # os.environ['ACCOUNT_REGION']
# key = "088488a3cf1c46e69292027802ac3d96" # os.environ['ACCOUNT_KEY']

# credentials = CognitiveServicesCredentials(key)
# client = ComputerVisionClient(
#     endpoint="https://" + region + ".api.cognitive.microsoft.com/",
#     credentials=credentials
# )

# def describe_image():
#     domain = "landmarks"
#     url = "http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg"
#     language = "en"
#     max_descriptions = 3

#     analysis = client.describe_image(url, max_descriptions, language)

#     for caption in analysis.captions:
#         print(caption.text)
#         print(caption.confidence)

# describe_image()

# import adal
# import requests
# import os
# import json


# endpoint = "https://whatever123.cognitiveservices.azure.com/"

# tenant = os.environ['TENANT']
# authority_url = 'https://login.microsoftonline.com/' + tenant
# client_id = os.environ['CLIENTID']
# client_secret = "088488a3cf1c46e69292027802ac3d96" # os.environ['CLIENTSECRET']
# resource = 'https://management.azure.com/'
# context = adal.AuthenticationContext(authority_url)
# token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
# headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
# # params = {'api-version': '2016-06-01'}
# params = {'url': "http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg"}
# # url = 'https://management.azure.com/' + 'subscriptions'
# url = endpoint + "/vision/v2.0/describe?language=en"

# r = requests.post(url, headers=headers, params=params)

# print(json.dumps(r.json(), indent=4, separators=(',', ': ')))

import requests
import os

subscription_key = "088488a3cf1c46e69292027802ac3d96"
endpoint = "https://whatever123.cognitiveservices.azure.com"
description_api_url = endpoint + "/vision/v2.0/describe" # "/text/analytics/v3.0/languages"

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(description_api_url, headers=headers, json={'url': "http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg"})
languages = response.json()
print(languages)
