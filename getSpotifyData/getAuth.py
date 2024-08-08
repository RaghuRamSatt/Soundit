import base64
import requests

"""
Gets a Spotify Auth token.
"""
def getAuth(id, secret):
    url="https://accounts.spotify.com/api/token"

    auth_header = base64.urlsafe_b64encode(f"{id}:{secret}".encode())
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % auth_header.decode()
    }

    payload = {
        'grant_type': 'client_credentials',
    }
    response = requests.post(url=url, data=payload, headers=headers)
    return response.json()["access_token"]

if __name__ == '__main__':
    getAuth('', '')

