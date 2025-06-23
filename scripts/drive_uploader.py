# scripts/drive_uploader.py

import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

import config

# Load from config.py
SERVICE_ACCOUNT_FILE = config.SERVICE_ACCOUNT_FILE
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = config.DRIVE_FOLDER_ID

def upload_to_drive(file_path='temp/generated_video.mp4', filename=None, mime_type='video/mp4'):
    print("[DEBUG] Starting Google Drive upload")

    # Check service account JSON file exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Missing service account file: {SERVICE_ACCOUNT_FILE}")

    # Check video file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video file not found: {file_path}")

    # Authenticate using service account
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    # Prepare file metadata
    file_metadata = {
        'name': filename or os.path.basename(file_path),
        'parents': [FOLDER_ID]
    }

    # Prepare media upload
    media = MediaFileUpload(file_path, mimetype=mime_type)
    print(f"[DEBUG] Uploading file: {file_path} to folder ID: {FOLDER_ID}")

    # Upload file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    print(f"[DEBUG] Uploaded file ID: {file['id']}")

    # Make the file publicly readable
    service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    print(f"[DEBUG] File shared publicly. Link: {file['webViewLink']}")

    return file.get('id'), file.get('webViewLink')
