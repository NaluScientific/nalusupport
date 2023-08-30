import argparse
import base64
import io
import json
import sys

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload


def main():
    """Downloads documents from the given drive folder as PDF, then
    uploads them to the given folder
    """
    args = parse_args(sys.argv[1:])
    folder_in_id = args.inid
    folder_out_id = args.outid
    drive_id = args.driveid
    credentials = load_credentials(args.credentials)

    file_ids = get_file_ids(folder_in_id, drive_id, credentials)
    for file_name, file_id in file_ids.items():
        print("Downloading as PDF:", file_name)
        contents = export_pdf(file_id, credentials)

        print("Uploading...")
        file_name += ".pdf"
        upload_or_update_pdf_from_memory(contents, file_name, folder_out_id, drive_id, credentials)


def load_credentials(encoded_creds: str) -> Credentials:
    """Base64 decodes the credentials, loads them as a json and returns
    Service Account Credentials
    """
    creds_str = base64.b64decode(encoded_creds)
    decoded = json.loads(creds_str)
    creds = service_account.Credentials.from_service_account_info(decoded)
    if not creds:
        raise ValueError("Invalid Credentials")
    return creds


def get_file_ids(parent_id: str, drive_id: str, creds: Credentials) -> dict:
    """Get all file ids in a given folder in Google Drive. Will not
    include folders. Duplicate file names will make me sad

    Args:
        parent_id (str): Google drive folder id to search in
        creds (Credentials): Service account credentials

    Returns:
        (dict) Mapping of file name (str) to file id (str)
    """
    try:
        service = build("drive", "v3", credentials=creds)
        filequery = f"parents in '{parent_id}' and not mimeType='application/vnd.google-apps.folder' and trashed=false"
        files = (
            service.files()
            .list(
                q=filequery,
                pageSize=1000,
                corpora="drive",
                driveId=drive_id,
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            ).execute()
        )
    except HttpError:
        raise
    file_ids = {drive_file["name"]: drive_file["id"] for drive_file in files["files"]}
    return file_ids


def upload_or_update_pdf_from_memory(
    contents: bytes, name: str, parent_id: str, drive_id: str, creds: Credentials
) -> str:
    """Uploads a file to parent_id, Updates the contents if file name exists at parent_id

    Args:
        contents (bytes): Bytes of file to upload
        name (str): Google drive file name
        parent_id (str): Id of parent folder to upload file to
        creds (Credentials): Service account credentials

    Returns:
        (str) File id of the uploaded/updated file
    """
    drive_file_ids = get_file_ids(parent_id, drive_id, creds)
    if name in drive_file_ids.keys():
        file_id = update_pdf_from_memory(contents, drive_file_ids[name], creds)
    else:
        file_id = upload_pdf_from_memory(contents, name, parent_id, creds)
    return file_id


def upload_pdf_from_memory(
    file_contents: bytes, file_name: str, parent_id: str, credentials: Credentials
) -> str:
    """Uploads a file to parent_id, Updates the contents if file name exists at parent_id
    Args:
        file_contents (bytes): Bytes of file to upload
        file_name (str): Google drive file name
        parent_id (str): Id of parent folder to upload file to
        credentials (Credentials): Service account credentials

    Returns:
        (str) File id of the uploaded/updated file
    """
    file_contents = io.BytesIO(file_contents)
    body = {"title": file_name, "name": file_name, "parents": [parent_id]}
    try:
        service = build("drive", "v3", credentials=credentials)
        media_body = MediaIoBaseUpload(
            file_contents,
            mimetype="application/pdf",
            chunksize=1024 * 1024,
            resumable=True,
        )
        file = (
            service.files()
            .create(
                body=body,
                media_body=media_body,
                supportsAllDrives=True,
                fields="id",
            )
            .execute()
        )
    except HttpError:
        raise
    return file.get("id")


def update_pdf_from_memory(
    file_contents: bytes, file_id: str, credentials: Credentials
):
    """Uploads a file to parent_id, Updates the contents if file name exists at parent_id
    Args:
        file_contents (bytes): Bytes of file to upload
        file_name (str): Google drive file name
        parent_id (str): Id of parent folder to upload file to
        credentials (Credentials): Service account credentials
    """
    try:
        service = build("drive", "v3", credentials=credentials)
        file_contents = io.BytesIO(file_contents)
        media_body = MediaIoBaseUpload(
            file_contents,
            mimetype="application/pdf",
            chunksize=1024 * 1024,
            resumable=True,
        )
        service.files().update(
            fileId=file_id,
            media_body=media_body,
            supportsAllDrives=True,
            keepRevisionForever=True,
        ).execute()
    except HttpError:
        raise


def export_pdf(file_id: str, credentials: Credentials) -> bytes:
    """Download a Document file in PDF format.

    Args:
        file_id: file ID of any workspace document format file
    Returns:
        IO object with location
    """
    try:
        service = build("drive", "v3", credentials=credentials)
        request = service.files().export_media(
            fileId=file_id, mimeType="application/pdf"
        )
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()
    except HttpError:
        raise

    return file.getvalue()


def parse_args(argv):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Upload file or folder contents to Google Drive"
    )
    parser.add_argument(
        "--credentials",
        "-c",
        type=str,
        required=True,
        help="Google Service Account Credentials",
    )
    parser.add_argument(
        "--driveid",
        type=str,
        required=True,
        help="Google drive top-level folder ID",
    )
    parser.add_argument(
        "--inid",
        "-i",
        type=str,
        required=True,
        help="Google Drive folder ID to download from",
    )
    parser.add_argument(
        "--outid",
        "-o",
        type=str,
        required=True,
        help="Google Drive folder ID to upload to",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    main()
