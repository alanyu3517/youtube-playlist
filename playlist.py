from pyasn1_modules.rfc2459 import NumericUserIdentifier
from Google import Create_Service
import pandas as pd

CLIENT_SECRET_FILE  =  'client_secret.json'
API_NAME  =  'youtube'
API_VERSION  =  'v3'
SCOPES  = ['https://www.googleapis.com/auth/youtube']

service =  Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

playlistId_Source = 'UU_Z1V8uaDMfwYQeIz8Keaxw'
playlistId_Target = 'PLHbpI0TsISORNoyfCBunSw__bBtVZyfKm'

response = service.playlistItems().list(
    part = 'contentDetails',
    playlistId = playlistId_Source,
    maxResults = 100,
).execute()

playlistItems = response['items']
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.playlistItems().list(
        part='contentDetails',
        playlistId=playlistId_Source,
        maxResults=50,
        pageToken=nextPageToken
    ).execute()

    playlistItems.extend(response['items'])
    nextPageToken = response.get('nextPageToken')

count = 0
newPlayList = []
for item in playlistItems:
    if item['contentDetails']['videoPublishedAt'] != '2019-04-02T10:57:27Z':
        newPlayList.insert(0, item)

newPlayList.sort(reverse=True, key=lambda e: e['contentDetails']['videoPublishedAt'])

for video in newPlayList:
    request_body = {
        'snippet': {
            'playlistId': playlistId_Target,
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': video['contentDetails']['videoId']
            }
        }
    }

    service.playlistItems().insert(
        part='snippet',
        body=request_body
    ).execute()
