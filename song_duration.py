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

#Call Mongo Instance
client = MongoClient()
db = client.now_playing
#Spotify Instance
client_data = {}
with open("secrets.json", 'r') as f:
    client_data = json.load(f)
client_credentials_manager = SpotifyClientCredentials(client_id=client_data["client_id"], client_secret=client_data["client_secret"],)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# In[0]:

print("Total number of Tweets: "+ str(db.cultural_tweet.find({}).count()))
print("Total number of Songs: " + str(len(db.cultural_tweet.distinct("track_title"))))
#print("Total number of Users: " + str(len(user_ids)))
print("Total number of Tweets with duration: "+ str(db.cultural_tweet.find({"duration_ms" : {"$exists": True}}).count()))
print("Total number of Tweets without duration: "+ str(db.cultural_tweet.find({"duration_ms" : {"$exists": False}}).count()))

# In[0]:
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_track_list(find_query):
    return db.cultural_tweet.find(find_query).distinct("track_id")

def get_complete_track(track):
    song_name = track["name"].lower()
    artist_name = " ".join(list(map(lambda x: x["name"], track["artists"]))).lower()
    return song_name + " " + artist_name

def get_searched_track_name(track):
    song_name = db.cultural_tweet.find_one({"track_id" : track}, {"track_title" : 1, "artist_name" : 1})
    return song_name["track_title"].lower() + " " + song_name["artist_name"].lower()

song_duration = -1
name_found = ""
searched_name = dict()
spotify_id = -1
track_list = get_track_list({"name_found" : {"$exists" : False }, "spotify_not_found" : {"$exists" : False }})
tracks_size = len(track_list)
searched = 0
for track in track_list:
    search_query = get_searched_track_name(track)
    search_result = sp.search(q = search_query, limit= 3, type="track")
    searched += 1
    score = 0
    for t in search_result["tracks"]["items"]:
        result_matcher = get_complete_track(t)
        similarity_score = similar(search_query,result_matcher)
        if(similarity_score > score):
            print("Found " + result_matcher + " => Similarity Score: " + str(similarity_score))
            song_duration = t["duration_ms"]
            score = similarity_score
            name_found = result_matcher
            searched_name[track] = search_query
            spotify_id = t["id"]
    print_text = ""
    if score > 0:
        db.cultural_tweet.update_many({"track_id": track},
        {"$set" : {
            "duration_ms" : song_duration,
            "spotify_id" : spotify_id,
            "similarity_score" : score,
            "name_found" : name_found
        }})
        print_text = " Saved song "+ name_found
    else:
         db.cultural_tweet.update_many({"track_id": track},
         {"$set" : {
             "spotify_not_found" : True
         }})
         print_text = " Not found in Spotify"
    print("Completed " + str(searched) +" out of " + str(tracks_size) + print_text)         
print("saved!")
    