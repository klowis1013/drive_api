from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
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

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, parents)").execute()
    items = results.get('files', [])
    page = results.get('nextPageToken', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            print(item['id'])

    i = 1
    while i <= 2:
        results = service.files().list(
            pageSize=10, pageToken=page, fields="nextPageToken, files(id, name, mimeType, parents)").execute()
        items = results.get('files', [])
        page = results.get('nextPageToken', [])

        if not items:
            break
        else:
            for item in items:
                print(u'{0}, {1}'.format(item['name'], item['id']))
        i += i

if __name__ == '__main__':
    main()