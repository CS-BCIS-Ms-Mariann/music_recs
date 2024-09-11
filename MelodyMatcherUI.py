import pandas as pd
import streamlit as st
from streamlit_pills import pills

st.set_page_config(page_title='Melody Matcher', page_icon="🎶", layout="wide",
                   initial_sidebar_state="collapsed", menu_items=None)

import StateManager as sm
import MelodyMatcher as mm

sm.set_session_states()

col1, col2, col3 = st.columns((2, 4, 2), gap="small")

with col1:
    st.image("images/rashid-khreiss-unsplash.jpg")
    st.caption('Photo by Rashid Khreiss on Unsplash')

with col2:
    st.markdown("<h1 style='text-align: center; color: #3266a8; font-size: 100px;'>Story Scout</h1>", unsafe_allow_html=True)
    st.divider()

with col3:
    st.image("images/rashid-khreiss-unsplash.jpg")
    st.caption('Photo by Rashid Khreiss on Unsplash')


st.subheader("Find Your Next Favorite Song!")
st.write()

# creates 3 columns and sets width of them
col = st.columns((3, 6), gap='medium')

with col[0]:

    st.subheader("1. Choose an artist")
    artists_list = mm.get_artists_list()
    artist = st.selectbox(
        label="Start Typing",
        options=artists_list,
        index=None,
        placeholder="Select an author..",
        key="author_select")

    st.session_state.artist = artist
    st.write(st.session_state.artist)

if st.session_state.artist != None and len(st.session_state.tracks) < 4:
    mm.new_tracks()

with col[1]:
    st.subheader("2. Choose a song")
    if len(st.session_state.tracks) > 0:
        chosen_track = pills(
        label="Select one",
        options=st.session_state.tracks,
        index=None,
        key="track_choice")

        st.session_state.track = chosen_track

    st.button("Get New Tracks", on_click=mm.new_tracks, key="refresh_tracks")

    if st.button("Submit Song", on_click=sm.add_track, key="submit_tracks"):
        st.write("You have submitted the rating!")


col1, col2 = st.columns((4, 4), gap='medium')
with col1:

    st.subheader("3. Get Your Recommendations")

    st.button("Get Recommendations", on_click=st.session_state.mm.get_results, key="recs")

    results = st.session_state.mm.get_recommendations()
    st.table(results)


# with col2:
#     reccs_lst = st.session_state.new_user.get_recs_list()
#     if len(reccs_lst) > 0:
#         reccs_df = sm.organize_reccs()
#         st.table(reccs_df)


