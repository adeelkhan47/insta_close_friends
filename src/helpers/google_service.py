import json
import os
import uuid
from fastapi import  HTTPException
from google.auth.transport.requests import Request


from google.oauth2.credentials import Credentials


# Function to get and refresh Google OAuth credentials
def get_google_credentials(creds_data):
    # Recreate credentials object from stored data
    creds = Credentials(
        token=creds_data['token'],
        refresh_token=creds_data['refresh_token'],
        token_uri=creds_data['token_uri'],
        client_id=creds_data['client_id'],
        client_secret=creds_data['client_secret'],
        scopes=creds_data['scopes']
    )

    # Check if token is expired and refresh if necessary
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        creds_data['token'] = creds.token  # Update token after refresh
        creds_data['expires_in'] = creds.expiry  # Update expiration time

    return creds