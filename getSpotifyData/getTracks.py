import requests
import pandas as pd
import json
from getAuth import getAuth


album_csv = "album_data.csv"
outfile = "track_data.csv"

def getTracks(ID, secret):
    auth_code = getAuth(ID, secret)
    df = pd.read_csv("artists.csv")
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer %s' % auth_code
    }  

    album_ids = []
    for index, row in df.iterrows():
        artist = row['Band Name']
        with open(f"artistAlbums/{artist}.json") as f:
            data = json.load(f)
            for album in data["items"]:
                id = album["id"]
                name = album["name"]
                album_ids.append((id, name))
    for album in album_ids:
        name = clean_name(album[1])
        id = album[0]
        url = f'https://api.spotify.com/v1/albums/{id}/tracks?offset=0'
        response = requests.get(url, headers=headers)
        with open(f"./albumsTracks/{name}.json", "w+") as f:
            json.dump(response.json(), f)


def clean_name(name):
    return name.replace("/", "")

if __name__ == '__main__':
    main()