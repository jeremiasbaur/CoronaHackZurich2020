import requests
import csv
import json
import time
from datetime import datetime

from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib import pyplot as plt

api_key = '35d1d908b96d4f3dc113e038eca30b53'

if __name__=='__main__':
    songs = {}
    
    if False:
        with open('Spotify/Latest_CH.csv', encoding="utf8") as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for line in reader:
                if line[5] in songs:
                    continue
                else:
                    songs[line[5]] = [line[6], line[7]]

        analyser = SentimentIntensityAnalyzer()

        i = 0
        chart_mean = 0
        for k, v in songs.items():
            print(k, v)

            payload = {'format'      : 'json',
                'page'        : 1,
                'page_size'   : 1,
                'q_artist'    : v[1],
                'q_track'      : v[0],
                }

            api_method_name = "track.search"
            api_url = "http://api.musixmatch.com/ws/1.1/" + api_method_name + "?apikey=" + api_key

            res = requests.get(api_url, params=payload) # hier kommt track_id zurück, musst du ausparsen

            #print(json.loads(res.text))
            if (json.loads(res.text)['message']['header']['status_code']!=200 or json.loads(res.text)['message']['header']['available']==0): continue

            track_id = json.loads(res.text)['message']['body']['track_list'][0]['track']['track_id']

            payload = {'format'      : 'json',
                        'track_id'    : track_id}

            api_method_name  = "track.lyrics.get"
            api_url = "http://api.musixmatch.com/ws/1.1/" + api_method_name + "?apikey=" + api_key
            res = requests.get(api_url, params=payload) # hier kommt Lyrics Body zurück

            try:
                lyrics = json.loads(res.text)['message']['body']['lyrics']['lyrics_body']
                #print(lyrics)
            except:
                continue
            
            mean = 0
            counter = 0
            counter_s = [0,0,0]

            for sentence in lyrics.split('\n'):
                if "*******" in sentence: continue
                score = analyser.polarity_scores(sentence)
                # print(sentence, "\t",score)
                mean += score['compound']
                counter += 1

                if -0.05 > score['compound']:
                    counter_s[0]+=1
                elif score['compound'] > 0.05:
                    counter_s[2]+=1
                else:
                    counter_s[1]+=1
            #print(mean/counter)

            songs[k].append(mean/counter)
            songs[k].append(counter_s)

            chart_mean += mean/counter

            i+=1
            #if i == 10:
            #    break

        chart_mean /= i

        print(chart_mean)

        with open("song_sentiment.json","w") as f:
            f.write(json.dumps(songs))

    song_data=None
    with open("TweetAnalysis/song_sentiment.json") as f:
        song_data=json.loads(f.read())
    
    chart_data={}
    with open('Spotify/Latest_CH.csv', encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            date = datetime.strptime(line[-1], "%Y-%m-%d")
            
            if len(song_data[line[5]])<3: continue
            if date in chart_data:
                chart_data[date].append(song_data[line[5]][2])
            else:
                chart_data[date] = [song_data[line[5]][2]]

    chart = []
    for k, v in chart_data.items():
        print(k, sum(v)/len(v))
        chart.append((sum(v)/len(v), k))

    plt.plot([i[1] for i in chart], [i[0] for i in chart])
    plt.show()