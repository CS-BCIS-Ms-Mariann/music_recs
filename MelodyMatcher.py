import pandas as pd
from sklearn.neighbors import NearestNeighbors
import streamlit as st
import pickle
import random


class MelodyMatcher:

    def __init__(self):
        self.features = ['danceability', 'energy', 'speechiness','acousticness', 'instrumentalness', 'valence', 'tempo']
        self.artist_list = get_artists_list()
        self.recommendations = None

    def get_results(self):
        '''
        Function: find songs most similar to given artist and song
        :param df: df containing data to make recommender from
        :param artist: name of artist to match from user
        :param title: name of song to match from user
        :param features: features used in creation of the model
        :param model: k_neighbors model
        :return: array with indexes of rows of most similar songs
        '''

        model = load_model('rec_system_model.sav')
        search_for = df.loc[
            (df['artist'] == st.session_state.artist) & (df['track'] == st.session_state.track)]
        target = search_for.loc[:, self.features].values
        results = model.kneighbors([target[0]])
        print(results)
        recommended = []
        for i in range(len(results[1][0])):
            index = results[1][0][i]
            artist = df.iloc[index]["artist"]
            title = df.iloc[index]["track"]
            if not(artist == 'Gorillaz'):
                recommended.append([artist, title])
        print(recommended)
        rec_results = pd.DataFrame(recommended, columns= ("artist", "title"))
        #print(rec_results)
        self.recommendations = rec_results

    def get_recommendations(self):
        print(self.recommendations)
        '''
        Function: outputs list of songs that are closest to given song in cluster
        :param results: list of results returned from model
        :return: None
        '''
        return self.recommendations

@st.cache_data()
def load_music_df(file_path):
    '''
    Function: create dataframe from csv file
    :param file_path: path to file with csv file
    :return: dataframe
    '''
    music_df = pd.read_csv(file_path)
    music_df = music_df.dropna()  # drop null values
    return music_df


path = "data/clean_music.csv"
df = load_music_df(path)

@st.cache_data()
def get_artists_list():
    '''
    :return: a list with all artists exactly once sorted in alphabetical order
    '''
    return sorted(list(df["artist"].unique()))  # creates a list of unique authors


@st.cache_data()
def create_artist_dict():
    '''
    Function: creates a dictionary with the artists as keys and a list of the titles
    of all the artists songs as values
    :return: a dictionary with artists as keys and a list of titles of all of their songs
    '''
    artist_dict = {}
    artist_list = get_artists_list()
    for artist in artist_list:
        track_df = df.loc[df["artist"] == artist]
        artist_dict[artist] = track_df["track"].to_list()
    return artist_dict


@st.cache_resource()
def create_model(features):
    '''
    Function: create model from dataframe
    :param df: dataframe containing data to make recommender from
    :param features: features to use in model
    :return: nearest neighbor model
    '''
    analyze = df.loc[:, features].values
    model = NearestNeighbors(n_neighbors = 5).fit(analyze)
    save_model(model, 'rec_system_model.sav')
    return model


def save_model(model, filename):
    # save the model to disk, not used in this program
    filename = 'rec_system_model.sav'
    pickle.dump(model, open(filename, 'wb'))


def load_model(filename):
    # load the model from disk, not used in this program
    model = pickle.load(open(filename, 'rb'))
    return model

def new_tracks():
    '''
    creates a new list of tracks to display for the users to choose from
    list is saved to session state
    '''
    # clears tracks that are stored in the session state
    if len(st.session_state.tracks) > 0:
        st.session_state.tracks.clear()
    artist_dict = create_artist_dict() # gets dictionary
    try:
        # gets list of all tracks from the dictionary
        tracks = artist_dict[st.session_state.artist]
        random.shuffle(tracks) #shuffles track so random songs will be chosen
        MAX = len(tracks)
        i = 0
        #iterates from 0 to MAX or 20 and adds songs to the list in the session state
        while i < MAX and i < 20:
            st.session_state.tracks.append(tracks[i])
            i += 1
    except KeyError:
        st.session_state.error = "Sorry, there as a problem"
        print(KeyError)


# features = ['Danceability', 'Energy', 'Speechiness','Acousticness', 'Instrumentalness', 'Valence', 'Tempo']
# df = read_file(path)
# model = create_model(df, features)
# song = input("What is the title of the song?") #'On Melancholy Hill'
# artist = input("Which artist created the song?") #'Gorillaz'
# results = create_target(df, artist, song , features, model)
# output_recommendations(results)