import os
import json
import re
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

path = "Spotify/Twitter Bunches"

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

count = 0

cleaned_tweets = []

c2 = 0
for tweet in tweets:
    #scores.append(analyser.polarity_scores(tweet['full_text']))
    date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y")

    scores[date.weekday()].append(analyser.polarity_scores(tweet['full_text'])['compound'])

    users.add(tweet['user']['id'])
    if (set(["corona", "covid", "Covid", "Corona", "COVID", "BAG", "Fälle", "Fallzahlen", "cases", "bag", "infection"]) 
        | set([i['text'] for i in tweet['entities']['hashtags']])) & set(tweet['full_text'].split()):
        count+=1
        #print(tweet['full_text'])

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
        #print(coords)

    cleaned_tweets.append({'text':tweet['full_text'], 'hashtags': [i['text'] for i in tweet['entities']['hashtags']], \
                            'date': date.__str__(), 'score': analyser.polarity_scores(tweet['full_text'])['compound'], \
                            'user': tweet['user']['id'], 'coords': coords})

    #print(cleaned_tweets[-1])
    
    #if tweet['coordinates'] is not None and tweet['geo'] is not None:
    #    print(tweet['place'], tweet['coordinates'], tweet['geo'])
        
#print(tweets[3456], len(tweets), len(users))

for i, data in enumerate(scores):
    overall = sum(data)
    
    d = stats.relfreq(data, numbins=20)
    #print(d)
    #plt.bar(np.arange(len(data)), d)
    #df = pd.DataFrame(data)
    #df.plot.hist(bins=20)
    
    #plt.plot(d.frequency)
    #plt.savefig(f'{i}.png')

print(count)

with open('cleaned_tweets.json', 'w') as f:
    f.write(json.dumps(cleaned_tweets))