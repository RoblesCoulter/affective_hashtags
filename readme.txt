CULTURAL #NOWPLAYING DATA
*********************************

This dataset contains data describing the listening events of users (extracted from the #nowplaying dataset), the emotion extracted from the hashtags used in the according tweets and information about the location of the user.


TWITTER AND TRACK DATA
-------------------------------
The data regarding the listening events is contained in np_cultural.zip and is encoded as json. It holds the following information:

- id: the id of the underlying tweet [*]
- user_id: the id of the user who sent the tweet (MD5 of it)
- user_lang: The BCP 47 code for the user’s self-declared user interface language. [*]
- user_time_zone: [*]
- text: actual content of the tweet [*]
- tweet_lang: language of the tweet (as detected by Twitter; BCP 47 language identifier corresponding to the machine-detected language of the Tweet text, or und if no language could be detected.) [*]
- geo: Deprecated version of coordinates (however, we deal with data stemming from before this API change, therefore we still include it; cf. coordinates for a description)
- coordinates: Represents the geographic location of this Tweet as reported by the user or client application. The inner coordinates array is formatted as geoJSON (longitude first, then latitude). [*]
- place: When present, indicates that the tweet is associated (but not necessarily originating from) a Place. [*]
- created_at: time the tweet was sent. [*]
- source: Utility used to post the Tweet, as an HTML-formatted string. [*]
- track_title: title of the track the user tweeted about
- track_id: the unique id of the track (from #nowplaying dataset) 
- artist_name: name of artist performing the track
- artist_id: the unique id of the artist (from #nowplaying dataset) 
- hashtags: list of hashtags used in the tweet.

[*] for further information about the information gathered from Twitter, please consult https://dev.twitter.com/overview/api/tweets

Please note that we do only add key-value pairs for geo/coordinates/place information if this information was provided by the Twitter API (i.e., missing keys signal that this information is not available for the given tweet).


SENTIMENT DATA
-------------------------------
The data regarding the hashtag's sentiment (if any could be obtained) is contained in np_cultural_sentiment.csv and is formatted as csv. The sentiment score was obtained by applying a set of well-known sentiment dictionaries. The sentiment scores are scaled between 0 and 1 (very negative to very positive). For each dictionary, we list the minimum, maximum, sum and average sentiment score across all hashtags used within every tweet (most tweets only feature a single hashtag we can assign a sentiment value to)
It contains the following information (in this particular order):
- name of the hashtag
- AFINN dictionary (min, max, sum, avg)
- Opinion Lexicon (min, max, sum, avg)
- Sentistrength Lexicon (min, max, sum, avg)
- Vader (min, max, sum, avg)
- Sentiment Hashtag Lexicon (min, max, sum, avg)


Please note that we only added hashtags for which we could obtain a sentiment value from at least one sentiment dictionary.


