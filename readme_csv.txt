README
nowplaying_csv.tar.gz 

This file contains a dump of the #nowplaying dataset which contains so-called listening events of users who publish the music they are currently listening to on Twitter. In particular, this dataset includes tracks which have been tweeted using the hashtags #nowplaying, #listento or #listeningto. In this dataset, we provide the track and artist of a listening event and metadata on the tweet (date sent, user, source). Furthermore, we provide a mapping of tracks and artists to its respective Musicbrainz identifiers.
The latest version of the dataset can be found at dbis-nowplaying.uibk.ac.at

This archive contains three csv-files:
1. nowplaying.csv: the main file which contains the following fields:
   - timestamp of the time the tweet underlying the listening event was sent
   - user id (each user is identified by a unique hash value)
   - source of the tweet (how it was sent; as provided by the Twitter API)
   - track title
   - artist name
   - track id (may be used to join this information with musicbrainz identifiers for artists and tracks as specified in mb_tracks.csv and mb_artists.csv)

2. mb_tracks.csv: contains a mapping of tracks to (possibly multiple) musicbrainz-identifiers for the track including the following two fields:
   - nowplaying track identifier
   - musicbrainz track identifier

3. mb_artists.csv: contains a mapping of artists to (possibly multiple) musicbrainz-identifiers for the artists including the following two fields:
   - nowplaying track identifier
   - musicbrainz artist identifier


In case you make use of our dataset in a scientific setting, we kindly ask you to cite the following paper (pdf can be gathered on dbis-nowplaying.uibk.ac.at: 
Eva Zangerle, Martin Pichl, Wolfgang Gassler, and Günther Specht. 2014. #nowplaying Music Dataset: Extracting Listening Behavior from Twitter. In Proceedings of the First International Workshop on Internet-Scale Multimedia Management (WISMM '14). ACM, New York, NY, USA, 21-26 

If you have any questions or suggestions regarding the dataset, please do not hesitate to contact Eva Zangerle (eva.zangerle@uibk.ac.at).
