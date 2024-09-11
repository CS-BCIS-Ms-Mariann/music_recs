import streamlit as st
import random
import pandas as pd
import MelodyMatcher as mm

st_s = st.session_state
def set_session_states():

    if "visibility" not in st_s:
        st_s.visibility = "visible"
        st_s.disabled = False

    if "artist" not in st_s:
        st_s.artist = ""

    if "track" not in st_s:
        st_s.track = ""

    if "tracks" not in st_s:
        st_s.tracks = []

    if "artists" not in st_s:
        st_s.artists = []

    if "error" not in st_s:
        st_s.error = "No error"

    if "mm" not in st_s:
        st_s.mm = mm.MelodyMatcher()

def clear_artist():
    del st_s.artist
    del st_s.track
    del st_s.artists
    del st_s.tracks
    st_s.error = "No Error"

def add_track():
    track = st_s.track

# def get_rated():
#     return st_s.new_user.get_t_rated()

# def organize_reccs():
#     recs_lst = st_s.new_user.recs_list
#     try:
#         reccs_df = pd.DataFrame(recs_lst, columns=("title", "author", "ave_rating"))
#         reccs_df.sort_values('ave_rating')
#         reccs_df = reccs_df[['title', 'author']]
#         return reccs_df.head(20)
#     except:
#         return recs_lst
