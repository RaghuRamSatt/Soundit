# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:29:20 2023

@author: raghu
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Fetch User Interaction Data
def fetch_user_interaction_data(engine):
    # Query to fetch user interaction data 
    query = """
    SELECT 
    User.username,
    COUNT(DISTINCT UserListensToTrack.track_id) AS total_tracks_listened,
    COUNT(DISTINCT UserFollowsArtist.artist_name) AS total_artists_followed,
    COUNT(DISTINCT UserFollowsPlaylist.playlist_id) AS total_playlists_followed
    FROM 
        User
    LEFT JOIN 
        UserListensToTrack ON User.username = UserListensToTrack.username
    LEFT JOIN 
        UserFollowsArtist ON User.username = UserFollowsArtist.username
    LEFT JOIN 
        UserFollowsPlaylist ON User.username = UserFollowsPlaylist.username
    GROUP BY 
        User.username
    """
    user_interaction_data = pd.read_sql(query, engine)
    return user_interaction_data


# Preprocess and Calculate Similarity

def preprocess_data(df):
    # Assuming 'username' is the only non-numeric column
    numeric_df = df.drop('username', axis=1)
    
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(numeric_df)
    return scaled_df


def calculate_user_similarity(preprocessed_df):
    similarity_matrix = cosine_similarity(preprocessed_df)
    return similarity_matrix


def update_user_similarity_scores(engine, users_df, similarity_matrix):
    for i in range(len(similarity_matrix)):
        for j in range(i + 1, len(similarity_matrix)):
            user1_id = users_df.iloc[i]['username']
            user2_id = users_df.iloc[j]['username']
            score = similarity_matrix[i][j]
            engine.execute(
                "INSERT INTO UserSimilarity (username1, username2, similarity_score) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE similarity_score = %s",
                (user1_id, user2_id, score, score)
            )

# Update Similarity Scores

def update_user_similarity_scores(engine, users_df, similarity_matrix):
    for i in range(len(similarity_matrix)):
        for j in range(i + 1, len(similarity_matrix)):
            user1_id = users_df.iloc[i]['username']
            user2_id = users_df.iloc[j]['username']
            score = similarity_matrix[i][j]
            engine.execute(
                "INSERT INTO UserSimilarity (username1, username2, similarity_score) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE similarity_score = %s",
                (user1_id, user2_id, score, score)
            )



def main():
    engine = create_engine('mysql+pymysql://root:password@localhost/soundit_test_2')

    # Fetch user data
    users_df = fetch_user_interaction_data(engine)

    # Preprocess data
    preprocessed_df = preprocess_data(users_df)

    # Calculate similarity scores
    user_similarity_matrix = calculate_user_similarity(preprocessed_df)

    # Update similarity scores in MySQL
    update_user_similarity_scores(engine, users_df, user_similarity_matrix)

