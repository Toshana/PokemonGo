# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:20:55 2016

@author: centraltendency
"""

import twitter
import json

CONSUMER_KEY = "Lm6isbqXBk1rz6yu2kfOyMWKV"
CONSUMER_SECRET = "2UjxjX86Lj0TLduyo3A7l7q0GoILHiIf2cjoYdXOIy4fhY8iPR"
OAUTH_TOKEN = "752924040365535232-KbCooprqT4gXaSZJmGA8lY54FDsMUDv"
OAUTH_TOKEN_SECRET = "v5ZqygMFgCT7KJficgO2rDNHU4GD0zCc8HdysvBdz01zr"

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

print(twitter_api)

WORLD_WOE_ID = 1
US_WOE_ID = 23424977

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
us_trends = twitter_api.trends.place(_id=US_WOE_ID)

# print(json.dumps(world_trends, indent=1))
# print(json.dumps(us_trends, indent=1))

world_trends_set = set([trend['name']
                        for trend in world_trends[0]['trends']])
                            
us_trends_set = set([trend['name']
                        for trend in us_trends[0]['trends']])
                            
common_trends = world_trends_set.intersection(us_trends_set)
print(common_trends)

pokemon = "#PokemonGO"
count = 100

pokemon_tweets = twitter_api.search.tweets(q=pokemon, count = count)

pokemon_statuses = pokemon_tweets['statuses']

# iterate through 5 more batches of results by following the cursor (?)

for _ in range(5):
    print("length of statuses", len(pokemon_statuses))
    try:
        next_results = pokemon_tweets['search_metadata']['next_results']
    except KeyError as e:
        break

    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
    
    pokemon_tweets = twitter_api.search.tweets(**kwargs)
    pokemon_statuses += pokemon_tweets['statuses']

# Show one sample search result by slicing the list...
print(json.dumps(pokemon_statuses[0], indent=1))

# extracting text, screen names, hashtags

status_texts = [status['text'] 
                   for status in pokemon_statuses]

screen_names = [user_mention['screen_name'] 
                    for status in pokemon_statuses 
                        for user_mention in status['entities']['user_mentions']]

hashtags = [hashtag['text']
            for status in pokemon_statuses
                for hashtag in status['entities']['hashtags']]
                    
# Compute a collection of all words from all tweets

words = [w
        for t in status_texts
            for w in t.split()]

# explore the first 5 items for each

print(json.dumps(status_texts[0:5], indent = 1))
print(json.dumps(screen_names[0:5], indent = 1))
print(json.dumps(hashtags[0:5], indent = 1))
print(json.dumps(words[0:5], indent = 1))

#creating a basic frequency distribution from the words in tweets

from collections import Counter

for item in [words, screen_names, hashtags]:
    c = Counter(item)
    print(c.most_common()[:10])
    
retweets = [(status['retweet_count'],
             status['retweeted_status']['user']['screen_name'],
             status['text'])
             for status in pokemon_statuses
                 if ('retweeted_status') in status
            ]
print(json.dumps(retweets[:5], indent = 1))


















