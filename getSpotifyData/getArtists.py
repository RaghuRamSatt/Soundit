import requests
import pandas as pd
import json
from getAuth import getAuth

artist_csv_name = 'artists.csv'
output_name = 'artist_data.csv'

spotify_endpoint = "https://api.spotify.com/v1/artists?ids="

def getArtists(ID, SECRET):
    df = pd.read_csv(artist_csv_name)
    artist_string = ''
    for row in df['ID']:
        artist_string = artist_string + str(row) + ','
    print("Getting auth code...")
    auth_code = getAuth(ID, SECRET)
    print("Auth code granted!")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer %s' % auth_code
    }
    print("Fetching artist data...")
    response_contents = requests.get(spotify_endpoint+artist_string,  headers=headers)
    print("Successfully fetched artist data from Spotify.")
    # cache the results
    with open("sampleArtists.json", "w+") as f:
        json.dump(response_contents.json(), f)

    print("Successfully wrote artist data to sampleArtists.json")
    
    requestBody = response_contents.json()
    print("Creating album files...")
    names = []
    for artist in requestBody["artists"]:
        if artist is None:
            continue
        name = artist['name']
        names.append(name)
    for name in names:
        with open("artistAlbums/"+name+'.json', 'w+') as f:
            f.write('')

    print("getArtists complete!")
    

        


if __name__ == '__main__':
    main()