import requests
import os
import json

import preprocessor as p

# Good Azure API Guide: https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python

subscription_key = os.environ['AzureSentKey']
endpoint = "https://twitter-emotion.cognitiveservices.azure.com/"
description_api_url = endpoint + "/vision/v2.0/describe" # "/text/analytics/v3.0/languages"
sentiment_api_url = endpoint + "/text/analytics/v3.0/sentiment"
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

    if response['errors']: # error list not empty
        raise response["errors"]

    return_val = [doc["confidenceScores"] for doc in response["documents"]]
    return return_val

def test_describe_image():
    url = "http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg"
    r = describe_image(url)
    print(r)

def test_sentiment_analysis():
    """texts = ["You are stupid",
                            "I hate my life",
                            "I love my life",
                            "We are here at hackzurich and our data is bad..",
                            "We are in Zurich",
                            "SRF is a media company",
                            "I sometimes like my life and situation but then there are also moments where I am completly lost",
                            "I am doing normal",
                            "Glencore is a mining company operating in Africa and other continents. They are often in the news for their actions regarding mining and exploiting children. This doesn't stop them from doing their usual business"]
    """

    texts = []

    start = 10000

    with open('Resources/topsecret/tweets_coords.json') as f:
        for i, row in enumerate(f.readlines()):
            if i<start: continue
            j = json.loads(row)
            
            texts.append(p.clean(j['full_text']))
            if (i>start+8): break
    
    print(sum([len(i) for i in texts])/len(texts))

    r = sentiment_analysis(texts)
    for i, results in enumerate(r):
        print(f'{i}\t{results}\tText: {texts[i]}')

if __name__=='__main__':
    test_sentiment_analysis()