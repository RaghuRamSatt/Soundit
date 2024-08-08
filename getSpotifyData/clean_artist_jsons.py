import pandas as pd
import json

artist_csv = "artist.csv"

def main():
    d = dict()
    d["name"] = []
    d["image"] = []
    with open("sampleArtists.json") as f:
        data = json.load(f)
        for artist in data["artists"]:
            if artist is not None:
                d["name"].append(artist["name"])
                d["image"].append(artist['images'][0]['url'])

    df = pd.DataFrame.from_dict(d)
    df.to_csv(artist_csv, index=False)

main()