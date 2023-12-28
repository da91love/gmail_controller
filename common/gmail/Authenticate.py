import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.modify']

class Authenticate:
    _instance = None  # Keep instance reference

    def __init__(self):
        self.auth = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def get_authenticate(self):
        if self.auth:
            return self.auth
        else:
            return self._create_authenticate()

    def _create_authenticate(self):
        creds = None
        if os.path.exists(project_root + '/token.json'):
            creds = Credentials.from_authorized_user_file(project_root + '/token.json')
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    project_root + "/common/public/input/credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open(project_root + '/token.json', 'w') as token:
                token.write(creds.to_json())
        return creds


    def test(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())