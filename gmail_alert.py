import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import json
import os

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# ✅ Inline credentials (replace with environment variables in production)
CLIENT_ID = "your_key"
CLIENT_SECRET = "your_key"
REDIRECT_URIS = ["http://localhost"]

# Gmail API service
def get_gmail_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uris": REDIRECT_URIS,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

# Build email message
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# Send the email if temperature triggers it
def send_email_if_temp_alert(temp_value):
    if 25 < temp_value < 30:
        service = get_gmail_service()
        message = create_message(
            sender="example@gmail.com",         # ⚠️ Replace with actual sender Gmail (must be the authorized user)
            to="sample5@gmail.com",         # ⚠️ Replace with actual recipient
            subject="🌡️ Temperature Alert",
            message_text=f"Alert! The current temperature is {temp_value}°C."
        )
        send_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Alert sent! Message ID: {send_message['id']}")
    else:
        print("Temperature is within normal range, no alert sent.")
