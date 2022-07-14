# Original file by Google LLC at
# https://github.com/googleworkspace/python-samples/blob/master/sheets/quickstart/quickstart.py
# Modified by @echedey-ls

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import threading

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSpreadSheetInterface(object):
    # pylint: disable=no-member
    def __init__(self, *, secrets_path, spreadsheet_id) -> None:
        self._secrets_path = secrets_path
        self._spreadsheet_id = spreadsheet_id
        self._scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self._action_underway = threading.Lock()
        # CREDENTIALS INITIALIZATION
        self._creds_path = os.path.join(self._secrets_path, 'credentials.json')
        self._token_path = os.path.join(self._secrets_path, 'token.json')
        self._creds = None
        # The file token.json stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists(self._token_path):
            self._creds = Credentials.from_authorized_user_file(
                self._token_path,
                self._scopes
            )
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            if (self._creds
                    and self._creds.expired
                    and self._creds.refresh_token):
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._creds_path,
                    self._scopes
                )
                self._creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self._token_path, 'w', encoding='utf-8') as token:
                token.write(self._creds.to_json())

    def read_range(self, range_: str) -> 'list[list]':
        ret_value = None
        try:
            self._action_underway.acquire()
            service = build('sheets', 'v4', credentials=self._creds)

            # Call the Sheets API
            # https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.values.html#get
            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self._spreadsheet_id,
                range=range_,
                majorDimension='ROWS',
                valueRenderOption='UNFORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING'
            ).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            ret_value = values
        except HttpError as err:
            print(err)
        finally:
            self._action_underway.release()
        return ret_value

    def update_range(self, range_: str, values: 'list[list]') -> dict:
        ret_value = None
        try:
            self._action_underway.acquire()
            service = build('sheets', 'v4', credentials=self._creds)

            # Call the Sheets API
            # https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.values.html#update
            sheet = service.spreadsheets()
            ret_value = sheet.values().update(
                spreadsheetId=self._spreadsheet_id,
                range=range_,
                valueInputOption='USER_ENTERED',
                body={
                    'values': values,
                    'majorDimension': 'ROWS'
                }
            ).execute()
        except HttpError as err:
            print(err)
        finally:
            self._action_underway.release()
        return ret_value
