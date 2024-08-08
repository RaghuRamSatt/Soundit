import pandas as pd
from datetime import datetime
import pymysql
from sqlalchemy import create_engine

# Function to convert date format for Album release_date
def convert_date(date_str):
    try:
        # Adjusting the format to match 'YYYY-MM-DD'
        converted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        print(f"Converting {date_str} to {converted_date}")
        return converted_date
    except ValueError as e:
        print(f"Error converting date: {date_str}. Error: {e}")
        return None


# Database connection string
connection_string = 'mysql+pymysql://root:test@localhost/soundit_test_2'
engine = create_engine(connection_string)

# --- Import Artist Data ---
try:
    df_artist = pd.read_csv('artist.csv')
    df_artist.to_sql('artist', con=engine, if_exists='append', index=False)
    print("Data from artist.csv successfully inserted into Artist")
except Exception as e:
    print(f"An error occurred while inserting Artist data: {e}")

# --- Import Album Data ---
try:
    df_album = pd.read_csv('album.csv')
    df_album['release_date'] = df_album['release_date'].apply(convert_date)
    df_album.to_sql('album', con=engine, if_exists='append', index=False)
    print("Data from album.csv successfully inserted into Album")
except Exception as e:
    print(f"An error occurred while inserting Album data: {e}")

# # --- Import Track Data ---
try:
    df_track = pd.read_csv('track.csv')
    df_album = pd.read_sql('SELECT album_id, name FROM Album', con=engine)
    album_name_id_map = dict(zip(df_album['name'], df_album['album_id']))
    df_track['album_id'] = df_track['album_name'].map(album_name_id_map)
    df_track = df_track.drop('album_name', axis=1)
    df_track.to_sql('track', con=engine, if_exists='append', index=False)
    print("Data from track.csv successfully inserted into Track")
except Exception as e:
    print(f"An error occurred while inserting Track data: {e}")

