# Sad music Naive Bayes classifier 

I wrote a summary about basics of naive bayes [here](https://kyungyunlee.github.io/archives/ML-study-Sad-Music-Naive-Bayes), if anyone is interested.        

Code contains a basic Gaussian Naive Bayes classifier for determining whether a given song is sad or happy. 

Data is from these 2 playlists. I took 100 songs from each playlist and trained a classifier with 30 songs out of 100. 
* [Sad playlist](https://open.spotify.com/playlist/54ozEbxQMa0OeozoSoRvcL?si=P2ODWYZ1S-Wo_IkFaSX8_A) 
* [Happy playlist](https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC?si=_bMVBft5REu2ge_e4bIfbg)

Attributes used are danceability, tempo, energy, valence and loudness. Below is a distribution of each attributes. Blue indicates sad songs, red indicates happy songs.    

![](dist.png)   

Test accuracy (70 songs per sad and happy songs) is around 93%, when trained with only 30 songs per class!!   


### Required
* Spotify Web API client information
  * Write down the info inside `spotify_secret.py`   
* [spotipy](https://github.com/plamere/spotipy) 
* basic libraries for data and ML stuff (ex. pandas, numpy, matplotlib, pickle, seaborn - for plotting) 

### How to train? 
```
python main.py --train
```
Statistics (mean,  standard deviation for each attributes) and prior probabilities (Y=sad, Y=not_sad) will be dumped inside `sad_naive_bayes.pkl` as a dictionary.  

```
summary = pickle.load(open('sad_naive_bayes.pkl', 'rb'))
''' 
summary['sad_prior'] : P(Y=sad)     
summary['happy_prior'] : P(Y=happy)    
summary['sad_stats']['danceability'] : [mean, std] for a gaussian distribution representing P(X=danceability|Y=sad)    
summary['happy_stats']['danceability'] : [mean, std] for a gaussian distribution representing P(X=danceability|Y=happy)     
'''
```

### How to predict?  
Type the following by putting any Spotify uri, like below 
```
python main.py --uri spotify:track:1vsTCdIbbVtKzj8t1uTMXH
```

### Reference 
* [https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/](https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/) 

