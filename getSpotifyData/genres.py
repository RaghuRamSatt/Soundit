import pandas as pd
import json
import os
genre_csv = 'track_genres.csv'

def main():
    d = dict()
    d["track_name"] = []
    d['genres'] = []

    
    df = pd.read_csv('track.csv')
    album_genres = pd.read_csv('album_genres.csv')

    for i, row in df.iterrows():
        album = row['album_name']
        genres = album_genres.loc[album_genres['album_name'] == album]['genres']
        if len(genres.values) > 0:
            d['track_name'].append(row['name'])
            d['genres'].append(genres.values[0])
        

    # for i, row in df.iterrows():
    #     artist = row['artist_name']
    #     genres = artist_genres.loc[artist_genres['name'] == artist]['genres'].values[0]
    #     print(genres)
    #     d['album_name'].append(row['name'])
    #     d['genres'].append(genres)

    # with open("sampleArtists.json") as f:
    #     data = json.load(f)
    #     for artist in data['artists']:
 
    #         d['genres'].append(artist['genres'])
    #         d['name'].append(artist['name'])

    
    df = pd.DataFrame.from_dict(d)
    df.to_csv(genre_csv, index=False)

if __name__ == '__main__':
    main()
