import os
import shutil
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from .config import Config


class GoogleAuth():
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]

    def authorization(self):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            if Config.DEPLOY_TYPE == "server_less":
                shutil.copyfile("token.json", "/tmp/token.json")
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            try:
                token_path = '/tmp/token.json' if Config.DEPLOY_TYPE == "server_less" else 'token.json'
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(e)
        return creds

    def close(self):
        os.remove('/tmp/token.json')
