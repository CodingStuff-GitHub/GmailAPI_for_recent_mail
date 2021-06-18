from __future__ import print_function
import os.path
import base64
import email
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

#Getting all the messages
def get_messages(service, user_id):
    try:
        return service.users().messages().list(userId=user_id).execute()
    except Exception as error:
        print("An error occurred: %s" % error)

#Getting single message
def get_message(service, user_id, msg_id):
    try:
        return (
            service.users()
                .messages()
                .get(userId=user_id, id=msg_id, format="metadata")
                .execute()
        )
    except Exception as error:
        print("An error occurred: %s" % error)

#Exposing the content of messages
def get_content_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
        msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
        mime_msg = email.message_from_string(msg_str)
        return mime_msg
    except Exception as error:
        print('An error occurred: %s' % error)


def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    # Call the Gmail API
    results = get_messages(service, "me")
    messages = results.get("messages", [])
    if not messages:
        print("No messages found.")
    else:
        print("Most Recent Email: ")
        message = messages[0]
        msg = get_content_message(service, "me", message["id"])
        print(msg)
        print("\n")


if __name__ == "__main__":
    main()
