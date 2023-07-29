from googleapiclient.discovery import build
from .google_auth import flow
from oauth2client.client import OAuth2Credentials
import httplib2

def create_calendar_service(user):
    credentials = OAuth2Credentials(access_token=user.profile.access_token,
                                    client_id=flow.client_id,
                                    client_secret=flow.client_secret,
                                    refresh_token=user.profile.refresh_token,
                                    token_uri=flow.token_uri)
    http_auth = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http_auth)
    return service