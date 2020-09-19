import os
import json
import re
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import tweepy

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def coordGetter(tweet):
    coords = []
    if tweet['geo'] is not None and tweet['geo']['type'] == 'Point':
        coords = [tweet['geo']['coordinates'][0], tweet['geo']['coordinates'][1]]
    elif 'bounding_box' in tweet['place'] and tweet['place']['bounding_box']['type'] == 'Polygon':
        coords = [0,0]
        for coord in tweet['place']['bounding_box']['coordinates'][0]:
            coords[0] += coord[1]
            coords[1] += coord[0]
        coords[0] /= len(tweet['place']['bounding_box']['coordinates'][0])
        coords[1] /= len(tweet['place']['bounding_box']['coordinates'][0])
    return coords


def keywordTweets(keywords, tweet):
    count = 0
    cleaned_tweets = []
    for tweet in tweets:
        #scores.append(analyser.polarity_scores(tweet['full_text']))
        date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y")

        scores[date.weekday()].append(analyser.polarity_scores(tweet['full_text'])['compound'])

        users.add(tweet['user']['id'])
        keyword_set = set([i.lower() for i in keywords])
        if (keyword_set & set(tweet['full_text'].lower().split()) or set([i['text'].lower() for i in tweet['entities']['hashtags']]) & keyword_set):
            count+=1

        coords=coordGetter(tweet)
        cleaned_tweets.append({'text':tweet['full_text'], 'hashtags': [i['text'] for i in tweet['entities']['hashtags']], \
                                'date': date.__str__(), 'score': analyser.polarity_scores(tweet['full_text'])['compound'], \
                                'user': tweet['user']['name'], 'screen_name': tweet['user']['screen_name'],\
                                 'coords': coords, 'tweetId': tweet['id_str'], 'langCode': tweet['lang']})

        #print(cleaned_tweets[-1])
    print(count)
    return cleaned_tweets

def tweet_query():
    #auth = tweepy.OAuthHandler(os.environ['TKEY_ONE'], os.environ['TKEY_TWO'])
    #auth.set_access_token(os.environ['TKEY_THREE'], os.environ['TKEY_FOUR'])
    auth = tweepy.OAuthHandler('B5Su4alcCwLloS9wRqDeR4hsR', 'e4tVP3LwAvc0BTbxyZGEH4ORefZ44GdtXqZ4bzvteSqI3HraM1')
    auth.set_access_token('2609885322-fk9REkBvsWmUSPPW3YUoab66Uj8jzjwQouXIgJG', 'u7n2JGFYgUttWKIvC6wAinVn3TVshoSY5fY5H8cnCPRgG')
    api = tweepy.API(auth, wait_on_rate_limit=True)

    searchTerms = ""
    noOfSearch = 200
    searchCountry = "Switzerland"
    places = api.geo_search(query=searchCountry, granularity="country")
    place_id = places[0].id

    d = tweepy.Cursor(api.user_timeline, id="twitter")
    print(d.items())
    tweets = []
    max_id = None
    for j in range(50):
        header = {
            "q": f'{searchTerms} place:{place_id}'.format(searchTerms, place_id) and ("place:%s" % place_id),
            "lang": "de",
            "tweet_mode": "extended",
            "count": 100,
            "max_id": max_id,
            "search_term": ""
        }
        try:
            batch_tweets = tweepy.Cursor(api.search, **header).items(noOfSearch)
        except Exception as error:
            break
        tweets.extend([i._json for i in batch_tweets])
        batch_ids = [i["id"] for i in batch_tweets]
        print(batch_tweets)
        #with open(f'TweetAnalysis/{j}_bunch.json', 'w', encoding='utf-8') as f:
        #    json.dump(batch_tweets, f, ensure_ascii=False)
        # lol()
        print(j)
        max_id = batch_ids[-1]
    return tweets


if __name__=='__main__':

    if True:
        path = "Spotify/Twitter Bunches/EN"
        tweets = []

        for file_name in os.listdir(path):
            with open(path+"/"+file_name, encoding="utf8") as f:
                for line in f.readlines():
                    tweets.extend(json.loads(line))


        analyser = SentimentIntensityAnalyzer()
        users = set()

        scores=[]
        for i in range(7):
            scores.append([])

        corona = ["corona", "covid", "covid", "COVID", "BAG", "Fälle", "Fallzahlen", "cases", "infection",'maskenpflicht','stayhomestaysafe','stayhome','distancing','covidiots']
        abstimmung = ["kampfjets",'armee','begrenzungsinitiative','svp','srf','initiative','abstimmung','streik']

        cleaned_tweets = keywordTweets(abstimmung , tweets)

        #print(cleaned_tweets)

        for i, data in enumerate(scores):
            overall = sum(data)
            
            d = stats.relfreq(data, numbins=20)
            #print(d)
            #plt.bar(np.arange(len(data)), d)
            #df = pd.DataFrame(data)
            #df.plot.hist(bins=20)
            
            #plt.plot(d.frequency)
            #plt.savefig(f'{i}.png')

        with open('TweetAnalysis/cleaned_tweets_en.json', 'w') as f:
            f.write(json.dumps(cleaned_tweets))

    if False:
        tweets = tweet_query()
        with open(f'TweetAnalysis/tweets.json', 'w', encoding='utf-8') as f:
            json.dump(tweets, f, ensure_ascii=False)
        