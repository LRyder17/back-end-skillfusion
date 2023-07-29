import os
from oauth2client.client import OAuth2WebServerFlow
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Get the credentials from environment variables
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='http://localhost:8000/oauth2callback/')
