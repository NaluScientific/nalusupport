from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import io


def authenticate():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    try:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    except FileNotFoundError:
        print("Please download the credentials.json file from https://console.cloud.google.com/apis/credentials and save it in the same directory as this script.")
        raise
    creds = flow.run_local_server(port=0)
    return creds


def get_existing_file_id(drive_service, filename, parent_folder_id):
    query = f"name='{filename}' and '{parent_folder_id}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query,
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        fields='files(id, name)'
    ).execute()
    files = results.get('files', [])
    return files[0]['id'] if files else None


def download_doc_as_pdf(drive_service, file_id):
    request = drive_service.files().export_media(fileId=file_id, mimeType='application/pdf')
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloaded {int(status.progress() * 100)}%")
    file_stream.seek(0)
    return file_stream


def upload_or_update_pdf(drive_service, file_stream, filename, shared_drive_folder_id):
    media = MediaIoBaseUpload(file_stream, mimetype='application/pdf')

    existing_file_id = get_existing_file_id(drive_service, filename, shared_drive_folder_id)

    if existing_file_id:
        uploaded_file = drive_service.files().update(
            fileId=existing_file_id,
            media_body=media,
            supportsAllDrives=True,
            fields='id'
        ).execute()
        print(f"Overwritten '{filename}' (file ID: {uploaded_file.get('id')})")
    else:
        file_metadata = {
            'name': filename,
            'parents': [shared_drive_folder_id],
        }
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            supportsAllDrives=True,
            fields='id'
        ).execute()
        print(f"Uploaded new file '{filename}' (file ID: {uploaded_file.get('id')})")

    return uploaded_file.get('id')
