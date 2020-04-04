import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import csv

# Import your spotify client id and client secret 
from spotify_secret import * 

client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

attributes = ['danceability', 'tempo', 'energy',  'key', 'valence', 'loudness', 'uri', 'trackname', 'artist', 'is_sad']  


def write_tracks(text_file, tracks):
    with open(text_file, 'a') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_url = track['uri']
                    # external_urls']['spotify']
                    file_out.write(track_url + '\n')
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def gather_data_from_spotify(): 
    
    results = sp.user_playlist('spotify', '37i9dQZF1DXdPec7aLTmlC',
                                    fields='tracks,next,name')

    text_file = 'happy.txt' 
    print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)

    results = sp.user_playlist('spotify', '54ozEbxQMa0OeozoSoRvcL',
                                        fields='tracks,next,name')

    text_file = 'sad.txt' 
    print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)


def make_data(n_train_sad, n_train_happy):
    # train 
    with open('is_this_sad.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=attributes)
        writer.writeheader()
        
        with open('happy.txt','r') as  f: 
            lines = f.readlines()
            for line in lines[:n_train_happy] :
                track_uri = line.strip('\n')

                features = sp.audio_features(track_uri)
                info = sp.track(track_uri)

                feat_dict = {}  
                for feature in features:
                    for att in attributes[:-4] : 
                        if att == 'key' : 
                            feat_dict[att] = int(feature[att])
                        else : 
                            feat_dict[att] = float(feature[att])
                feat_dict['trackname'] = info['name']
                feat_dict['artist'] = info['artists'][0]['name']
                feat_dict['uri'] =track_uri
                feat_dict['is_sad'] = 0
                print (feat_dict)
                writer.writerow(feat_dict) 

     
        with open('sad.txt','r') as  f: 
            lines = f.readlines()
            for line in lines[:n_train_sad] :
                track_uri = line.strip('\n')

                features = sp.audio_features(track_uri)
                info = sp.track(track_uri)

                feat_dict = {}  
                for feature in features:
                    for att in attributes[:-4] : 
                        feat_dict[att] = feature[att]
                feat_dict['trackname'] = info['name']
                feat_dict['artist'] = info['artists'][0]['name']
                feat_dict['uri'] =track_uri
                feat_dict['is_sad'] = 1
                print (feat_dict)
                writer.writerow(feat_dict) 


    # test    
    with open('is_this_sad_test.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=attributes)
        writer.writeheader()
        
        with open('happy.txt','r') as  f: 
            lines = f.readlines()
            for line in lines[n_train_happy:] :
                track_uri = line.strip('\n')

                features = sp.audio_features(track_uri)
                info = sp.track(track_uri)

                feat_dict = {}  
                for feature in features:
                    for att in attributes[:-4] : 
                        if att == 'key' : 
                            feat_dict[att] = int(feature[att])
                        else : 
                            feat_dict[att] = float(feature[att])
                feat_dict['trackname'] = info['name']
                feat_dict['artist'] = info['artists'][0]['name']
                feat_dict['uri'] =track_uri
                feat_dict['is_sad'] = 0
                print (feat_dict)
                writer.writerow(feat_dict) 

     
        with open('sad.txt','r') as  f: 
            lines = f.readlines()
            for line in lines[n_train_sad:] :
                track_uri = line.strip('\n')

                features = sp.audio_features(track_uri)
                info = sp.track(track_uri)

                feat_dict = {}  
                for feature in features:
                    for att in attributes[:-4] : 
                        feat_dict[att] = feature[att]
                feat_dict['trackname'] = info['name']
                feat_dict['artist'] = info['artists'][0]['name']
                feat_dict['uri'] =track_uri
                feat_dict['is_sad'] = 1
                print (feat_dict)
                writer.writerow(feat_dict) 



if __name__ == '__main__' : 

    gather_data_from_spotify()
    make_data(30, 30) 
