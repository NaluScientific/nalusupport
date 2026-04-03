from googleapiclient.discovery import build
import yaml

from drive_utils import authenticate, download_doc_as_pdf, upload_or_update_pdf

GUIDES_FILE = './_data/guides.yml'
SHARED_DRIVE_FOLDER_ID = '1qoIsDQK2y-ISr8261MjqMj5YXE_T9zj_'

DOCUMENTS = {
    "AARDVARCv3 Self (signal) Triggering Guide": {
        "id": "19420ZUgXIG-wMbP-rJwqWKmvU5l-7U5cQcowAWMGwKY",
    },
    "AARDVARCv3 coincidence triggering guide": {
        "id": "1LdHHY-PKuTMgUac_BanAz4GX8T6MfX4tKgNMw_Ra6Oc",
    },
    "User Guide: Pedestals": {
        "id": "1lTEQlSkwmalnIVL6GWs-3Jk3rZ0Quero5SYbtiRPwrs",
    },
    "User Guide: Configuring Clock Tree": {
        "id": "16fekWireSzHPT-dyZnNIVZQm38OIF9Fe3kigvR8F2mg",
    },
}


def main():
    """Export guide Google Docs as PDFs, upload to shared Drive, and update guides.yml URLs."""
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)

    with open(GUIDES_FILE, 'r') as file:
        guides = yaml.safe_load(file)

    for guide_name, item in DOCUMENTS.items():
        doc_file_id = item['id']
        if not doc_file_id:
            print(f"Skipping '{guide_name}' (no doc id)")
            continue

        pdf_name = f"{guide_name}.pdf"
        print(f"Processing: {pdf_name}")
        pdf_stream = download_doc_as_pdf(drive_service, doc_file_id)
        file_id = upload_or_update_pdf(drive_service, pdf_stream, pdf_name, SHARED_DRIVE_FOLDER_ID)
        file_link = f"https://drive.google.com/file/d/{file_id}/view?usp=drive_link"
        for guide in guides:
            if guide["name"] == guide_name:
                guide["url"] = file_link

    with open(GUIDES_FILE, 'w') as file:
        yaml.dump(guides, file, default_flow_style=False, allow_unicode=True)


if __name__ == '__main__':
    main()
