# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:42:56 2023

@author: raghu
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np

# Database connection string
connection_string = 'mysql+pymysql://root:password@localhost/soundit_test_2'
engine = create_engine(connection_string)

def fetch_users(engine):
    # Fetch user data from the database
    query = "SELECT username FROM User"
    users_df = pd.read_sql(query, engine)
    return users_df

def update_user_similarity_scores(engine, users_df):
    for i in range(len(users_df)):
        user1_id = users_df.iloc[i]['username']
        for j in range(i + 1, len(users_df)):
            user2_id = users_df.iloc[j]['username']
            score = np.random.rand()  # Random score
            # Insert or update the similarity score
            engine.execute(
                "INSERT INTO UserSimilarity (username1, username2, similarity_score) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE similarity_score = %s",
                (user1_id, user2_id, score, score)
            )

def main():
    engine = create_engine(connection_string)

    # Fetch user data
    users_df = fetch_users(engine)

    # Update user similarity scores with random values
    update_user_similarity_scores(engine, users_df)

# Run the process
main()