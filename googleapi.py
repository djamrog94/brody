import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build
from httplib2 import Http
from random import randint
# from urllib import urlopen
# from urllib3 import request, urlopen
import json

CLIENT_SECRET = 'client_secret.json'
SCOPE = 'https://www.googleapis.com/auth/photoslibrary.readonly'
STORAGE = Storage('credentials.storage')

with open('g_cred.txt', 'r') as f:
    ID = f.readline().rstrip()


# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials


def get_photos():
    credentials = authorize_credentials()
    gdriveservice = build('photoslibrary', 'v1', http=credentials.authorize(Http()))
    results = gdriveservice.mediaItems().search(body={'pageSize': 100, 'albumId': ID}).execute()
    items = results.get('mediaItems', [])
    loop_list = []
    total_list = []
    for item in items:
        try:
            loop_list = [item['baseUrl'], item['id'], item['mediaMetadata']['creationTime']]
        except:
            break
        total_list.append(loop_list)
        # print('{} {} {}'.format(item['productUrl'], item['id'], item['mediaMetadata']['creationTime']))
    random_number = randint(0, len(total_list)-1)
    history = open("history_total.txt", "r")
    history_db = history.read()
    history = open("history_total.txt", "a+")
    while str(random_number) in history_db:
        random_number = randint(0, len(total_list) - 1)
    history.write(str(random_number)+'\n')
    history.close()
    url = total_list[random_number][0]
    photo_id = total_list[random_number][1]
    date = total_list[random_number][2]
    return date, url, photo_id


def get_specific(photo_id):
    credentials = authorize_credentials()
    gdriveservice = build('photoslibrary', 'v1', http=credentials.authorize(Http()))

    nextpagetoken = 'Dummy'
    while nextpagetoken != '':
        nextpagetoken = '' if nextpagetoken == 'Dummy' else nextpagetoken
        results = gdriveservice.mediaItems().search(body={'albumId': ID, "pageToken": nextpagetoken}).execute()
        items = results.get('mediaItems', [])
        nextpagetoken = results.get('nextPageToken', '')
        for item in items:
            if item['id'] == photo_id:
                return item['baseUrl']
