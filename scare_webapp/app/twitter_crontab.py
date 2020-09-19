"""from app import app, db, crontab

import tweepy
import os

@crontab.job(minute='0', hour='6')
def tweet_query():
    auth = tweepy.OAuthHandler(os.environ['TKEY_ONE'], os.environ['TKEY_TWO'])
    auth.set_access_token(os.environ['TKEY_THREE'], os.environ['TKEY_FOUR'])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    searchTerms = ""
    noOfSearch = 200
    searchCountry = "Switzerland"
    places = api.geo_search(query=searchCountry, granularity="country")
    place_id = places[0].id

    max_id = None
    for j in range(50):
        header = {
            "q": f'{searchTerms} place:{place_id}'.format(searchTerms, place_id) and ("place:%s" % place_id),
            "lang": "en",
            "tweet_mode": "extended",
            "count": 100,
            "max_id": max_id,
            "search_term": ""
        }
        try:
            batch_tweets = tweepy.Cursor(api.search, **header).items(noOfSearch)
        except Exception as error:
            break
        batch_tweets = [i._json for i in batch_tweets]
        batch_ids = [i["id"] for i in batch_tweets]
        with open(f'TweetAnalysis/{j}_bunch.json', 'w', encoding='utf-8') as f:
            json.dump(batch_tweets, f, ensure_ascii=False)
        # lol()
        max_id = batch_ids[-1]


if __name__=='__main__':
    tweet_query()"""