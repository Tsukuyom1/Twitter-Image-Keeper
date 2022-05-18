from .config import Config

import re
from .google_auth import GoogleAuth

from pprint import pprint

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheets():

    GOOGLE_DRIVE_ROOT_DIR = Config.GOOGLE_DRIVE_ROOT_DIR

    def update(self, tweets):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = GoogleAuth().authorization()

        try:
            service = build('sheets', 'v4', credentials=creds)

            drive_sheet_id = self.create_sheet(creds, 'result', self.GOOGLE_DRIVE_ROOT_DIR)
            print('sheet_id', drive_sheet_id)
            sheet_id = self.get_file_metadata(drive_sheet_id, creds)
            pprint(sheet_id)

            insert_column = []
            for tweet in tweets:
                insert_column.append([tweet['created_at'], tweet['screen_name'], tweet['name'], tweet['tweet_url']])
            print(insert_column)
            request = service.spreadsheets().values().append(spreadsheetId=sheet_id, range='A1',
                                                             valueInputOption='USER_ENTERED',
                                                             body={
                                                                 'values': insert_column,
                                                                 "majorDimension": "ROWS"}
                                                             ).execute()
            pprint(request)
        except HttpError as err:
            print(err)

    def create_sheet(self, creds, title, parents_name):
        drive_service = build('drive', 'v3', credentials=creds)
        root_dir_id = self.get_file_id(parents_name, drive_service)
        sheet_id = self.get_file_id(title, drive_service)
        if sheet_id:
            print('Sheet already exists. ID: {}'.format(sheet_id))
            return sheet_id
        body = {
            'name': title,
            'parents': [root_dir_id],
            'mimeType': 'application/vnd.google-apps.spreadsheet',
        }
        spreadsheet = drive_service.files().create(body=body, fields='id').execute()
        return spreadsheet.get('id')

    def get_file_id(self, title, service):

        results = service.files().list(
            pageSize=100, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            return
        for item in items:
            if item['name'] == title:
                return item['id']
        return None

    def get_file_metadata(self, id, creds):
        drive_service = build('drive', 'v3', credentials=creds)
        try:
            metadata = drive_service.files().get(fileId=id, fields='*').execute()
            r = r'https://docs.google.com/spreadsheets/d/([^/]*)/edit.*'
            m = re.match(r, metadata['webViewLink'])

            return m.groups(1)[0]
        except HttpError as err:
            print(err)
