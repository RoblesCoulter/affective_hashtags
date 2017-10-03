
# coding: utf-8

# In[ ]:




# # CULTURAL #NOWPLAYING DATA
# *********************************
# 
# This dataset contains data describing the listening events of users (extracted from the #nowplaying dataset), the emotion extracted from the hashtags used in the according tweets and information about the location of the user.
# 
# 
# TWITTER AND TRACK DATA
# -------------------------------
# The data regarding the listening events is contained in np_cultural.zip and is encoded as json. It holds the following information:
# 
# - id: the id of the underlying tweet [*]
# - user_id: the id of the user who sent the tweet (MD5 of it)
# - user_lang: The BCP 47 code for the user’s self-declared user interface language. [*]
# - user_time_zone: [*]
# - text: actual content of the tweet [*]
# - tweet_lang: language of the tweet (as detected by Twitter; BCP 47 language identifier corresponding to the machine-detected language of the Tweet text, or und if no language could be detected.) [*]
# - geo: Deprecated version of coordinates (however, we deal with data stemming from before this API change, therefore we still include it; cf. coordinates for a description)
# - coordinates: Represents the geographic location of this Tweet as reported by the user or client application. The inner coordinates array is formatted as geoJSON (longitude first, then latitude). [*]
# - place: When present, indicates that the tweet is associated (but not necessarily originating from) a Place. [*]
# - created_at: time the tweet was sent. [*]
# - source: Utility used to post the Tweet, as an HTML-formatted string. [*]
# - track_title: title of the track the user tweeted about
# - track_id: the unique id of the track (from #nowplaying dataset) 
# - artist_name: name of artist performing the track
# - artist_id: the unique id of the artist (from #nowplaying dataset) 
# - hashtags: list of hashtags used in the tweet.
# 
# [*] for further information about the information gathered from Twitter, please consult https://dev.twitter.com/overview/api/tweets
# 
# Please note that we do only add key-value pairs for geo/coordinates/place information if this information was provided by the Twitter API (i.e., missing keys signal that this information is not available for the given tweet).
# 
# 
# SENTIMENT DATA
# -------------------------------
# The data regarding the hashtag's sentiment (if any could be obtained) is contained in np_cultural_sentiment.csv and is formatted as csv. The sentiment score was obtained by applying a set of well-known sentiment dictionaries. The sentiment scores are scaled between 0 and 1 (very negative to very positive). For each dictionary, we list the minimum, maximum, sum and average sentiment score across all hashtags used within every tweet (most tweets only feature a single hashtag we can assign a sentiment value to)
# It contains the following information (in this particular order):
# - name of the hashtag
# - AFINN dictionary (min, max, sum, avg)
# - Opinion Lexicon (min, max, sum, avg)
# - Sentistrength Lexicon (min, max, sum, avg)
# - Vader (min, max, sum, avg)
# - Sentiment Hashtag Lexicon (min, max, sum, avg)
# 
# 
# Please note that we only added hashtags for which we could obtain a sentiment value from at least one sentiment dictionary.

# In[35]:

import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np 
import json
import csv
import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from difflib import SequenceMatcher


# In[36]:

#Call Mongo Instance
client = MongoClient()
db = client.now_playing

#Spotify Instance
client_credentials_manager = SpotifyClientCredentials(client_id="7736d10450e04c5f9e302bb07a4f6cf7", client_secret="a11e29bc5c324ddeb19fc6249d303814",)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# In[37]:

## NowPlaying Cultural Sentiment Data
"""
cs_header = ["hashtag", "AFINN_min", "AFINN_max", "AFINN_sum", "AFINN_avg", "OpinionLex_min", "OpinionLex_max", "OpinionLex_sum", "OpinionLex_avg", "Sentistrength_min", "Sentistrength_max", "Sentistrength_sum", "Sentistrength_avg", "Vader_min", "Vader_max", "Vader_sum", "Vader_avg", "SentimentHashtag_min", "SentimentHashtag_max", "SentimentHashtag_sum", "SentimentHashtag_avg"]
np_cs = pd.read_csv('np_cultural_sentiment.csv',names = cs_header)
"""
#IMPORTING Cultural Sentiment Data to MongoDB
"""
np_cs_json = json.loads(np_cs.to_json(orient="records"))
db.cultural_sentiment.drop()
db.cultural_sentiment.insert_many(np_cs_json)
"""


# In[38]:

## Transformation of NowPlaying Cultural Tweets to DataframeStructure
"""
output = []
with open("np_cultural.json") as f:
    for line in f:     
        output.append(json.loads(line))
np_c = pd.DataFrame(output)
"""
#IMPORTING Cultural Tweets to MongoDB
"""
db.cultural_tweet.drop()
records = json.loads(np_c.T.to_json()).values()
db.cultural_tweet.insert_many(records)
"""


# ### Importing the MusicBrainz Mapping of artists and tracks
# 
# `mongoimport -d now_playing -c mb_tracks --type csv --file mb_tracks.csv --fields "np_id,mb_track_id"`
# 
# `mongoimport -d now_playing -c mb_artists --type csv --file mb_artists.csv --fields "np_id,mb_artist_id"`

# In[39]:

## Transformation and Importing of Playlist Data from NowPlaying to MongoDB
"""
np_pl = pd.read_csv("playlist.csv", names=["playlist_id","track_id","playlist_name"])
np_pl_json = json.loads(np_pl.to_json(orient="records"))
db.playlist.drop()
db.playlist.insert_many(np_pl_json)
"""


# In[ ]:




# In[48]:

#db.cultural_tweet.find({"hashtag": "nobeats"})
user_tweets = db.cultural_tweet.find({"user_id": '1c10f9788fdcc4baf6cf6a2631fe78bc12102418'})
#TOTAL Number of Tweets
print("Total number of Tweets: "+ str(db.cultural_tweet.find({}).count()))
print("Total number of Songs: " + str(len(db.cultural_tweet.distinct("track_title"))))
#Get Distinct User Ids
print("Total number of Users: " + str(len(user_ids)))


# In[51]:

user_ids = db.cultural_tweet.distinct("user_id")
type(user_ids)


# In[60]:

first = user_ids[0]
user_songs = db.cultural_tweet.find({"user_id": first})
initial_song = user_songs[1]
initial_date = initial_song["created_at"]


# In[61]:

db.mb_tracks.find({"np_id": initial_song["track_id"]}).count()
initial_song


# In[62]:

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def convertMillis(millis):
     seconds=(millis/1000)%60
     minutes=(millis/(1000*60))%60
     return str(int(seconds)), str(int(minutes))


# In[64]:

search_query = initial_song["track_title"] +" "+ initial_song["artist_name"]
results = sp.search(q=search_query,limit=3)
print("Looking for: "+initial_song["track_title"] + " " + initial_song["artist_name"])
for track in results["tracks"]["items"]:
    print(track["name"])
    print(track["artists"][0]["name"]) 
    print(track["duration_ms"])
    result_matcher = 


# In[22]:



#Get Spotify's song duration
track_list = db.cultural_tweet.distinct("track_id")
p = 0
for track in track_list:
    song_name = db.cultural_tweet.find_one({"track_id": track}, {"track_title" : 1 , "artist_name": 1})
    result = sp.search(q= song_name["artist_name"].lower() + " " + song_name["track_title"].lower() ,limit= 3, type="track")
    print("Looking for:" + song_name["track_title"].lower() + " - " + song_name["artist_name"].lower())
    for t in result["tracks"]["items"]:
        print(t["name"] + " _ " + t["artists"][0]["name"])
        s,m = convertMillis(t["duration_ms"])
        print(m + ":" + s)
    print("__________________________")
    p = p+1
    if p > 20:
        break


# In[13]:

p = 0
for track in track_list:
    song_name = db.cultural_tweet.find_one({"track_id": track}, {"track_title" : 1 , "artist_name": 1})
    print(song_name["track_title"])
    print(song_name["artist_name"])
    print("______________________")
    p = p+1
    if p> 20:
        break


# In[ ]:



