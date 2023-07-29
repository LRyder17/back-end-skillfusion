import json
from oauth2client.client import OAuth2WebServerFlow

with open('/Users/SRyder/Documents/ada/Core/Capstone/back-end-skillfusion/credentials/credentials.json', 'r') as file:
    credentials = json.load(file)

flow = OAuth2WebServerFlow(client_id=credentials['web']['client_id'],
                        client_secret=credentials['web']['client_secret'],
                        scope='https://www.googleapis.com/auth/calendar',
                        redirect_uri='http://localhost:8000/oauth2callback/')
