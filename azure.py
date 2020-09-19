import requests
import os

# Good Azure API Guide: https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python

subscription_key = "088488a3cf1c46e69292027802ac3d96"
endpoint = "https://whatever123.cognitiveservices.azure.com"
description_api_url = endpoint + "/vision/v2.0/describe" # "/text/analytics/v3.0/languages"
sentiment_api_url = endpoint + "/text/analytics/v2.0/sentiment"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}

def describe_image(image_url="http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg"):
    # https://docs.microsoft.com/en-us/rest/api/cognitiveservices/computervision/describeimage/describeimage
    response = requests.post(description_api_url, headers=headers, json={'url': image_url})
    return_val = response.json()
    assert type(return_val) is str
    return return_val

def sentiment_analysis(sentences, lang="en"):
    """ Takes a list of Strings
        Returns a list of scores from 0 to 1: 0 negative, 1 postive """
    # https://docs.microsoft.com/en-us/rest/api/cognitiveservices/textanalytics/sentiment/sentiment

    assert type(sentences) is list

    json_body = {"documents": []}

    for i, sentence in enumerate(sentences):
        json_body["documents"].append({"id": i, "text": sentence, "language": lang})
    
    response = requests.post(sentiment_api_url, headers=headers, json=json_body)
    response = response.json()

    if response["errors"]: # error list not empty
        raise response["errors"]

    return_val = [doc["score"] for doc in response["documents"]]
    return return_val

def test_sentiment_analysis():
    r = sentiment_analysis(["You are stupid", "I hate my life", "I love my life"])
    print(r)