# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 20:46:16 2023

@author: raghu
"""


#     The script connects to the MySQL database using create_engine.
#     get_last_processed_id function retrieves the ID of the last track that was processed for similarity scoring.
#     update_last_processed_id function updates this ID in the TrackSimilarityProgress table after processing new tracks.
#     update_similarity_scores is the main function that retrieves new tracks (those that haven't been processed yet), computes random similarity scores for each pair of new tracks, and updates these scores in the database.
#     After processing, the script updates the last processed track ID in the database.

#  This setup ensures that each time you run the script, it only processes new tracks added to the database since the last run, enhancing efficiency.

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np

# Database connection string
connection_string = 'mysql+pymysql://root:password@localhost/soundit_test_2'
engine = create_engine(connection_string)

def get_last_processed_id(engine):
    with engine.connect() as conn:
        result = conn.execute("SELECT IFNULL(MAX(last_processed_track_id), 0) FROM TrackSimilarityProgress")
        last_id = result.scalar()
    return last_id

def update_last_processed_id(engine, last_id):
    with engine.connect() as conn:
        conn.execute("REPLACE INTO TrackSimilarityProgress (last_processed_track_id) VALUES (%s)", (last_id,))

def update_similarity_scores(engine):
    last_processed_id = get_last_processed_id(engine)

    with engine.connect() as conn:
        new_tracks = pd.read_sql(f"SELECT track_id FROM Track WHERE track_id > {last_processed_id}", conn)

        if not new_tracks.empty:
            for i in range(len(new_tracks)):
                track1_id = new_tracks.iloc[i]['track_id']
                for j in range(i + 1, len(new_tracks)):
                    track2_id = new_tracks.iloc[j]['track_id']
                    # Check if this pair already exists
                    pair_exists = conn.execute("SELECT COUNT(*) FROM TrackSimilarity WHERE track_id1 = %s AND track_id2 = %s", (track1_id, track2_id)).scalar()
                    if not pair_exists:
                        score = np.random.rand()  # Random score for illustration
                        # Insert similarity score
                        conn.execute("INSERT INTO TrackSimilarity (track_id1, track_id2, similarity_score) VALUES (%s, %s, %s)", (track1_id, track2_id, score))

                # Update the last processed track ID after each track1_id is fully processed
                update_last_processed_id(engine, track1_id)

# Run the update process
update_similarity_scores(engine)


