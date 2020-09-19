import requests
import os

# Good Azure API Guide: https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python

subscription_key = os.environ['AZURE_KEY']
endpoint_name = os.environ['AZURE_ENDPOINT']
assert subscription_key, "AZURE_KEY environment variable not set!"
assert endpoint_name, "AZURE_ENDPOINT environment variable not set!"

endpoint = "https://" + endpoint_name + ".cognitiveservices.azure.com"
description_api_url = endpoint + "/vision/v2.0/describe"
sentiment_api_url = endpoint + "/text/analytics/v2.0/sentiment"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}

def describe_image(image_url):
    # https://docs.microsoft.com/en-us/rest/api/cognitiveservices/computervision/describeimage/describeimage
    response = requests.post(description_api_url, headers=headers, json={'url': image_url})
    return_val = response.json()
    return_val = ". ".join([x["text"] for x in return_val["description"]["captions"]])
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

def test_describe_image():
    url = "http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg"
    r = describe_image(url)
    print(r)

def test_sentiment_analysis():
    r = sentiment_analysis(["You are stupid", "I hate my life", "I love my life", "You are smarter than a dog. But not much"])
    print(r)

test_sentiment_analysis()