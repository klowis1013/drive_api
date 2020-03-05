from __future__ import print_function  # python2에서 python3을 사용하기 위해
import pickle  # 텍스트 이외의 자료형을 파일로 저장하기 위하여
import os.path  # 작업디렉토리의 경로변경 등을 위해
from googleapiclient.discovery import build
''' Google API 클라이언트 라이브러리. HTTP 및 JASON을 기반으로 작성.
직접 HTTP요청을 설정하고 응답을 파싱해야 하는 번거로움을 없애줌.'''
from google_auth_oauthlib.flow import InstalledAppFlow  # 사용자인증 위해
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# (the file token.pickle에 대한 설명은 밑에서 찾아봐. creds변수 밑에 있음.)
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# 서로 다른 종류의 동작과 작업요청들의 모음에는 서로 다른 스코프가 필요


def main():
    """Shows basic usage of the Drive v3 API.
    버젼 3 드라이브 API를 기초용례를 보여주겠다.
    Prints the names and ids of the first 10 files the user has access to.
    첫 10개 파일의 이름과 식별변호를 찍어주마.
    """
    creds = None  # None은 값의 부재를 나타내는 내장 상수
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.(token.pickle은 처음 접속했을때 자동으로 생성되었다.)
    if os.path.exists('token.pickle'):  # (조건문에는 콜론, 토큰피클이 있으면)"
        with open('token.pickle', 'rb') as token:
            # with는 파일 여닫이, as는 =이퀄, 즉 변수정의"
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
        # files 객체  https://developers.google.com/drive/api/v3/reference/files"
        pageSize=10,
        fields="files(createdTime, id, name, mimeType, parents)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} {1}, {2}, {3}'.format(
                item['name'],
                item['createdTime'], item['id'], item['parents']))

if __name__ == '__main__':
    main()
