import os
from oauth2client.client import OAuth2WebServerFlow
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

django_env = os.getenv('DJANGO_ENV', 'development')

if django_env == 'production':
    redirect_uri = 'https://skillfusion-db.onrender.com/oauth2callback/'
else:
    redirect_uri = 'http://localhost:8000/oauth2callback/'

# Get the credentials from environment variables
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri=redirect_uri)
