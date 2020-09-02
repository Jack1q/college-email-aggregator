from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64 # for decoding messages
import csv
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)

def crawl_mail(service, id, token='', mail=[]):
    response = service.users().messages().list(userId='me',pageToken=token).execute()
    for message in response['messages']:
        msg = service.users().messages().get(userId='me',id=message['id']).execute()
        try:
            msg_data = str(base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data'].encode('UTF8')))
            if len(sys.argv) == 1 or (sys.argv[1] == 'waiver-only' and 'waiver' in msg_data):
                for x in msg['payload']['headers']:
                    if x['name'] == 'From':
                        sender_email = x['value'][x['value'].index('<')+1:x['value'].rindex('>')].strip()
                        if sender_email.endswith('.edu'):
                            with open('data.csv','a+',newline='') as data_file:
                                csv.writer(data_file, delimiter=',').writerow([sender_email, msg_data])
        except:
            pass
    if 'nextPageToken' in response:
        return crawl_mail(service, id, response['nextPageToken'], mail)
    return ''
crawl_mail(service, id='me')