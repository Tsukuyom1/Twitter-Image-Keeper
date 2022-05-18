from __future__ import print_function
from .config import Config
from .google_auth import GoogleAuth

import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class GoogleDrive():

    GOOGLE_DRIVE_ROOT_DIR = Config.GOOGLE_DRIVE_ROOT_DIR

    def upload(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """

        creds = GoogleAuth().authorization()

        try:
            # Call the Drive v3 API
            drive_service = build('drive', 'v3', credentials=creds)

            # Create root folder
            root_dir_id = self.create_folder(drive_service, self.GOOGLE_DRIVE_ROOT_DIR)

            # Upload files
            dir_path = '/tmp/images' if Config.DEPLOY_TYPE == "server_less" else 'files/images'
            for file_name in os.listdir(dir_path):
                print('Uploading file: {}'.format(file_name))
                self.upload_file(drive_service, file_name, root_dir_id)

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def upload_file(self, drive_service, file_name, root_dir_id):
        child_path = file_name.split('_')[0]
        child_path_id = self.create_folder(drive_service, child_path, root_dir_id)
        print('child_path_id', child_path_id)
        if self.get_folder_id(drive_service, file_name):
            print('File already exists. ID: {}'.format(file_name))
            return
        file_metadata = {'name': file_name, 'parents': [child_path_id]}
        # media = MediaFileUpload('./images/' + file_name, mimetype='image/jpeg')
        media = MediaFileUpload('/tmp/images/' + file_name, mimetype='image/jpeg')
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))

    def create_folder(self, drive_service, folder_name, parents=None):
        folder_id = self.get_folder_id(drive_service, folder_name)
        if folder_id:
            print('Folder or File already exists. ID: {}'.format(folder_id))
            return folder_id
        print('Creating folder')
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        if parents:
            file_metadata['parents'] = [parents]
        file = drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        print('Folder ID: %s' % file.get('id'))
        return file.get('id')

    def get_folder_id(self, drive_service, folder_name):
        results = drive_service.files().list(
            pageSize=100, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            return
        for item in items:
            if item['name'] == folder_name:
                return item['id']
        return None
