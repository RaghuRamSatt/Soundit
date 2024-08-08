import pandas as pd
import json
import os

album_csv = "album.csv"

def main():
    d = dict()
    d["name"] = []
    d["image"] = []
    d["release_date"] = []
    d["artist_name"] = []

    directoryName = "artistAlbums"
    directory = os.fsencode(directoryName)
    
    for file in os.listdir(directory):
        filename = directoryName + "/" + os.fsdecode(file)
        with open(filename) as f:
            data = json.load(f)
            for album in data["items"]:
                d["name"].append(album["name"])
                d["image"].append(album["images"][0]["url"])
                d["artist_name"].append(album["artists"][0]["name"])
                d["release_date"].append(album["release_date"])

    df = pd.DataFrame.from_dict(d)
    df.to_csv(album_csv, index=False)


main()