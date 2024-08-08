import pandas as pd
import requests
import json
from getAuth import getAuth

artists_csv = 'artists.csv'
outfile = "album_data.csv"


def getAlbums(ID, secret):
    print("Getting authorization for albums...")
    auth_code = getAuth(ID, secret)
    if auth_code is not None:
        print("Successfully got authorization!")
    else:
        print("Error getting authorization!")
        exit -1

    df = pd.read_csv(artists_csv)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer %s' % auth_code
    }

    for index, row in df.iterrows():
        id = row['ID']
        name = row["Band Name"]
        url = f'https://api.spotify.com/v1/artists/{id}/albums?include_groups=album&limit=5&offset=0'
        response = requests.get(url, headers=headers)
        with open(f"artistAlbums/{name}.json", "w+") as f:
            json.dump(response.json(), f)
            



if __name__ == '__main__':
    main()