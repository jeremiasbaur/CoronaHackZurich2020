import requests
import os

# Good Azure API Guide: https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python

subscription_key = "088488a3cf1c46e69292027802ac3d96"
endpoint = "https://whatever123.cognitiveservices.azure.com"
description_api_url = endpoint + "/vision/v2.0/describe" # "/text/analytics/v3.0/languages"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}

def describe_image(image_url="http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg")
    response = requests.post(description_api_url, headers=headers, json={'url': image_url})
    return response.json()
