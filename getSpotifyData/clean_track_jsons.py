import pandas as pd
import json
import os

track_csv = "track.csv"

def main():
    d = dict()
    d["name"] = []
    d["duration"] = []
    d["file_path"] = []
    d["album_name"] = []

    directoryName = "albumsTracks"
    directory = os.fsencode(directoryName)
    
    for file in os.listdir(directory):
        filename = directoryName + "/" + os.fsdecode(file)
        album_name = os.fsdecode(file).split(".")[0]
        with open(filename) as f:
            data = json.load(f)
            for track in data["items"]:
                d["name"].append(track["name"])
                d["album_name"].append(album_name)
                d["duration"].append(track["duration_ms"])
                d["file_path"].append(track["preview_url"])

    df = pd.DataFrame.from_dict(d)
    df.to_csv(track_csv, index=False)

main()