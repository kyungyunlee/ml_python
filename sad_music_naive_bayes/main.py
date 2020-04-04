import os 
import sys 
import pandas as pd 
import numpy as np 
import math 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from spotify_secret import *




# Gaussian distribution
def calculate_probability(x, mean, stdev):
    exponent = math.exp(-((x-mean)**2 / (2 * stdev**2 )))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

# Calculate the probability that an observed X is in class_Y
def class_probability(sad_prior, happy_prior, sad_stats, happy_stats, observed_data) :
    sad_prob = sad_prior
    happy_prob = happy_prior 
    for i, val in enumerate(observed_data) : 
        sad_prob *= calculate_probability(val, sad_stats[attributes[i]][0], sad_stats[attributes[i]][1])
        happy_prob *= calculate_probability(val, happy_stats[attributes[i]][0], happy_stats[attributes[i]][1])

    return sad_prob, happy_prob
    
        
# Predict whether the given feature is a sad song or happy song 
def predict(sad_prior, happy_prior, sad_stats, happy_stats, observed_data): 
    sad_prob, happy_prob = class_probability(sad_prior, happy_prior, sad_stats, happy_stats, observed_data)
    if sad_prob > happy_prob : 
        return 1 
    else :
        return 0 


def naive_bayes(train_df, test_df):

    sad_songs = []
    happy_songs = [] 

    sad_df = train_df.loc[train_df['is_sad'] == 1]
    happy_df = train_df.loc[train_df['is_sad'] == 0]

    for index, rows in sad_df.iterrows() : 
        feat = [rows.danceability, rows.tempo, rows.energy, rows.valence, rows.loudness]
        sad_songs.append(feat)


    for index, rows in happy_df.iterrows() : 
        feat = [rows.danceability, rows.tempo, rows.energy, rows.valence, rows.loudness]
        happy_songs.append(feat)

    sad_songs = np.array(sad_songs)
    happy_songs = np.array(happy_songs)


    # Mean and standard deviation of each attributes when Y=sad or Y=not_sad
    sad_song_stats = {}
    happy_song_stats = {} 
    print ("Sad song stats")
    for i, att in enumerate(attributes):
        print (att) 
        mu = np.mean(sad_songs[:, i])
        std = np.std(sad_songs[:, i])
        print (mu,std)
        sad_song_stats[att] = [mu,std]
    print ()
    print ("Happy song stats")
    for i, att in enumerate(attributes):
        print (att) 
        mu = np.mean(happy_songs[:, i])
        std = np.std(happy_songs[:, i])
        print (mu,std)
        happy_song_stats[att] = [mu,std] 
    print () 
    # compute prior Y 
    sad_prior = train_df[train_df.is_sad == 0].shape[0] / train_df.shape[0]
    happy_prior = train_df[train_df.is_sad == 1].shape[0] / train_df.shape[0]
    
    # Test 
    n_correct = 0 
    for index, rows in test_df.iterrows() : 

        feat = [rows.danceability, rows.tempo, rows.energy, rows.valence, rows.loudness]
        label = predict(sad_prior, happy_prior, sad_song_stats, happy_song_stats, feat)
        if label == rows['is_sad'] : 
            n_correct += 1 
        else :
            print ("Wrong tracks")

            print (rows['trackname'], "predicted as {}, correct is {}".format(label, rows['is_sad']) )

    acc = n_correct / test_df.shape[0]
    print ()
    print ("Accuracy : %f"%acc)
    return {"sad_prior" : sad_prior,
            "happy_prior" : happy_prior,
            "sad_stats" : sad_song_stats,
            "happy_stats" : happy_song_stats} 



def is_it_sad(track_uri, summary):

    client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    attributes = ['danceability', 'tempo', 'energy',  'key', 'valence', 'loudness', 'uri', 'trackname', 'artist', 'is_sad']

    features = sp.audio_features(track_uri) 
    # track_uri = track_uri.split(":")[-1]
    # info = sp.tracks(track_uri)
    # print (info)
    feat_dict = {}
    for feature in features : 
        for att in attributes[:-4]: 
            feat_dict[att] = feature[att]

        # feat_dict['trackname'] = info['name']
        # feat_dict['artist'] = info['artists'][0]['name']
        feat_dict['uri'] = track_uri
        feat_dict['is_sad'] = 0

    input_feature = [feat_dict['danceability'], feat_dict['tempo'], feat_dict['energy'], feat_dict['valence'], feat_dict['loudness']] 

    predicted_label = predict(summary['sad_prior'], summary['happy_prior'], summary['sad_stats'], summary['happy_stats'], input_feature ) 
    if predicted_label == 1 : 
        # print (" {} by {} is a sad song".format(feat_dict['trackname'], feat_dict['artist']))
        print ("Boohoo the song is sad :'(")
    else :
        # print (" {} by {} is a happy song".format(feat_dict['trackname'], feat_dict['artist']))
        print ("Yaaay the song is happy :D")

if __name__ == '__main__' : 

    import pickle 
    import argparse 

    parser = argparse.ArgumentParser()
    parser.add_argument('--uri', type=str)
    parser.add_argument('--train', action='store_true')
    
    args = parser.parse_args()

    attributes = ['danceability', 'tempo','energy', 'valence', 'loudness'] 



    if args.train : 
        train_df = pd.read_csv('is_this_sad.csv', index_col='uri', header=0)
        test_df = pd.read_csv('is_this_sad_test.csv', index_col='uri', header=0)
        summary = naive_bayes(train_df, test_df)
        pickle.dump(summary, open('sad_naive_bayes.pkl','wb')) 
        print ("Stats dumped at 'sad_naive_bayes.pkl'")
    else : 
        if not os.path.exists('sad_naive_bayes.pkl') : 
            train_df = pd.read_csv('is_this_sad.csv', index_col='uri', header=0)
            test_df = pd.read_csv('is_this_sad_test.csv', index_col='uri', header=0)
            print ("need to train a classifier") 
            summary = naive_bayes(train_df, test_df)
        else :  
            summary = pickle.load(open('sad_naive_bayes.pkl', 'rb'))
    
    if args.uri  : 
        is_it_sad(args.uri, summary) 
    else : 
        print ("Indicate a spotify track uri by calling python main.py --uri spotify_track_uri") 

