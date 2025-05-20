from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.oauth2.credentials import Credentials
import yaml
import io

BOARDS_FILE = './_data/board.yml'

DOCUMENTS = {
    "aardvarcv3": {
        "id": "1BqGZal_IOrkoO7TrRUAlaFkhiINsB95hPEwgifx6xJA",
        "name": "AARDVARCv3 Quick Start Guide",
    },
    "asocv3": {
        "id": "1vmIQJW7kLYbjM9UroSmDwvjUb4p3xHjRvwRLp2V06uA",
        "name": "ASOCv3 Quick Start Guide",
    },
    "dsa-c10-8": {
        "id": "1lNx10sOix7dyMLdyyJDC4lHss2JILCN850cH5ig14bc",
        "name": "DSA-C10-8 Quick Start Guide",
    },
    "hdsocv2_evalr2": {
        "id": "1L7TGPs3nOFr6QudJ0OP8-9_vvB_9UeZN6ExA69bH7pg",
        "name": "HDSOCv2 Eval Rev2 Quick Start Guide",
    },
}

def authenticate():
    # OAuth 2.0 flow (interactive, no saved token file)
    SCOPES = ['https://www.googleapis.com/auth/drive']
    try:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    except FileNotFoundError:
        print("Please download the credentials.json file from https://console.cloud.google.com/apis/credentials and save it in the same directory as this script.")
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
        # Overwrite existing file
        uploaded_file = drive_service.files().update(
            fileId=existing_file_id,
            media_body=media,
            supportsAllDrives=True,
            fields='id'
        ).execute()
        print(f"Overwritten '{filename}' (file ID: {uploaded_file.get('id')})")
    else:
        # Upload new file
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

def main():
    """A script to update the Quick Start Guide PDFs for the AARDVARCv3 board.
    
    For each document in DOCUMENTS dictionary open the google drive doc.
    Check if it exists in the shared drive folder, if it exists, overwrite, if not upload a new version.


    
    """
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)
    # Replace this with your Shared Drive folder ID
    shared_drive_folder_id = '14hBAGJ9ni-QwqH_7yAbrO45Yd_k_baxA'

    with open(BOARDS_FILE, 'r') as file:
        brd_yml = yaml.safe_load(file)

    for brd_name, item in DOCUMENTS.items():
        pdf_name = f"{item['name']}.pdf"
        doc_file_id = item['id']
        print(f"Processing: {pdf_name}")
        pdf_stream = download_doc_as_pdf(drive_service, doc_file_id)
        file_id = upload_or_update_pdf(drive_service, pdf_stream, pdf_name, shared_drive_folder_id)
        file_link = f"https://drive.google.com/file/d/{file_id}/view?usp=drive_link"
        for brd_item in brd_yml[brd_name]["current"]:
            print(brd_item["name"])
            if brd_item["name"] == "Quick Start Guide (PDF)":
                brd_item["url"] = file_link
    # Write the updated configuration back to the file
    with open(BOARDS_FILE, 'w') as file:
        yaml.dump(brd_yml, file, default_flow_style=False)

if __name__ == '__main__':
    main()
