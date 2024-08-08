# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 18:56:14 2023

@author: raghu
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import ast

# Function to transform genre list strings into actual lists
def parse_genre_list(genre_list_str):
    try:
        return ast.literal_eval(genre_list_str)
    except ValueError:
        return []

# Database connection string
connection_string = 'mysql+pymysql://root:test@localhost/soundit_test_2'
engine = create_engine(connection_string)

# Read CSV files
df_track_genres = pd.read_csv('track_genres.csv')
df_album_genres = pd.read_csv('album_genres.csv')

# Transform genre data
df_track_genres['genres'] = df_track_genres['genres'].apply(parse_genre_list)
df_album_genres['genres'] = df_album_genres['genres'].apply(parse_genre_list)

# Create a unique set of genres
unique_genres = set()
for genres in df_track_genres['genres'].tolist() + df_album_genres['genres'].tolist():
    unique_genres.update(genres)

# Insert unique genres into the Genre table
for genre in unique_genres:
    try:
        engine.execute(f"INSERT IGNORE INTO Genre (name) VALUES ('{genre}');")
    except Exception as e:
        print(f"An error occurred while inserting genre '{genre}': {e}")

# Map genre names to genre IDs
df_genre = pd.read_sql('SELECT genre_id, name FROM Genre', con=engine)
genre_name_id_map = dict(zip(df_genre['name'], df_genre['genre_id']))

# Map tracks and albums to their respective IDs
df_track = pd.read_sql('SELECT track_id, name FROM Track', con=engine)
df_album = pd.read_sql('SELECT album_id, name FROM Album', con=engine)
track_name_id_map = dict(zip(df_track['name'], df_track['track_id']))
album_name_id_map = dict(zip(df_album['name'], df_album['album_id']))

# Insert genre-track and genre-album relationships
for _, row in df_track_genres.iterrows():
    track_id = track_name_id_map.get(row['track_name'])
    if track_id:
        for genre in row['genres']:
            genre_id = genre_name_id_map.get(genre)
            if genre_id:
                try:
                    engine.execute(f"INSERT IGNORE INTO GenreCategorizesTrack (genre_id, track_id) VALUES ({genre_id}, {track_id});")
                except Exception as e:
                    print(f"An error occurred while inserting genre-track relationship: {e}")

for _, row in df_album_genres.iterrows():
    album_id = album_name_id_map.get(row['album_name'])
    if album_id:
        for genre in row['genres']:
            genre_id = genre_name_id_map.get(genre)
            if genre_id:
                try:
                    engine.execute(f"INSERT IGNORE INTO GenreCategorizesAlbum (genre_id, album_id) VALUES ({genre_id}, {album_id});")
                except Exception as e:
                    print(f"An error occurred while inserting genre-album relationship: {e}")
