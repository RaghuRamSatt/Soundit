from getArtists import getArtists
from getAlbums import getAlbums
from getTracks import getTracks
from getAuth import getAuth
from clean_artist_jsons import main as cleanArtists
from clean_album_jsons import main as cleanAlbums
from clean_track_jsons import main as cleanTracks

ID=''
SECRET=''

"""
To use, get an appication ID and secret key from the spotify developer portal, fill that data into the constant
variables at the top of this file, and execute it. Ensure that there is an albumsTracks folder and artistAlbums folder in the same directory.
Also, ensure that an artists.csv file exists with one column named "ID" that contains spotify IDs of artists.
"""
def main():
    getArtists(ID, SECRET)
    getAlbums(ID, SECRET)
    getTracks(ID, SECRET)
    cleanArtists()
    cleanAlbums()
    cleanTracks()