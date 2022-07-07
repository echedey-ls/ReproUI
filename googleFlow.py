# Original file by Google LLC at https://github.com/googleworkspace/python-samples/blob/master/sheets/quickstart/quickstart.py
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

class googleSpreadSheetInterface(object):
    def __init__(self, *, secretsPath, spreadSheetId) -> None:
        self._secretsPath   = secretsPath
        self._spreadSheetId = spreadSheetId
        self._scopes   = ['https://www.googleapis.com/auth/spreadsheets']
        self._actionUnderway = threading.Lock()
        ## CREDENTIALS INITIALIZATION
        self._credsPath = os.path.join(self._secretsPath, 'credentials.json')
        self._tokenPath = os.path.join(self._secretsPath, 'token.json')
        self._creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self._tokenPath):
            self._creds = Credentials.from_authorized_user_file(self._tokenPath, self._scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._credsPath, 
                    self._scopes
                )
                self._creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self._tokenPath, 'w') as token:
                token.write(self._creds.to_json())
    def readRange(self, range: str) -> list[list]:
        retVal = None
        try:
            self._actionUnderway.acquire()
            service = build('sheets', 'v4', credentials=self._creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId= self._spreadSheetId,
                range= range,
                majorDimension= 'ROWS'
            ).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            retVal = values
        except Exception as err:
            print(err)
        finally:
            self._actionUnderway.release()
            return retVal

    def updateRange(self, range: str, values: list[list]) -> dict | None:
        retVal = None
        try:
            self._actionUnderway.acquire()
            service = build('sheets', 'v4', credentials=self._creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            retVal = sheet.values().update(
                spreadsheetId= self._spreadSheetId,
                range= range,
                valueInputOption = 'USER_ENTERED',
                body= {
                    'values': values,
                    'majorDimension': 'ROWS'
                }
            ).execute()
        except Exception as err:
            print(err)
        finally:
            self._actionUnderway.release()
            return retVal
