import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class OAuthHandler:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    def get_authorization_url(self):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri="urn:ietf:wg:oauth:2.0:oob"
        )
        auth_url, _ = flow.authorization_url(prompt="consent")
        return auth_url

    def exchange_code_for_tokens(self, code):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri="urn:ietf:wg:oauth:2.0:oob"
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        return {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

    def get_credentials(self, token_info):
        credentials = Credentials.from_authorized_user_info(token_info, self.scopes)
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        return credentials
