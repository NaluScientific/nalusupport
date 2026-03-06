from googleapiclient.discovery import build
import yaml

from drive_utils import authenticate, download_doc_as_pdf, upload_or_update_pdf

BOARDS_FILE = './_data/board.yml'
SHARED_DRIVE_FOLDER_ID = '14hBAGJ9ni-QwqH_7yAbrO45Yd_k_baxA'

DOCUMENTS = {
    "asocv3": {
        "id": "17jg5gcy4MRN0rAS5YPjU7adMRuwmjSiLWimHnu-JJCQ",
        "name": "ASOCv3 Product Sheet",
    },
    "dsa-c10-8": {
        "id": "1OjFxIZoI6Wdx5ySPHrBdaBNsRtvWaXEq218ZwFj_Eeo",
        "name": "DSA-C10-8 Product Sheet",
    }
}


def main():
    """Export Product Sheet Google Docs as PDFs, upload to shared Drive, and update board.yml URLs."""
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)

    with open(BOARDS_FILE, 'r') as file:
        brd_yml = yaml.safe_load(file)

    for brd_name, item in DOCUMENTS.items():
        pdf_name = f"{item['name']}.pdf"
        doc_file_id = item['id']
        print(f"Processing: {pdf_name}")
        pdf_stream = download_doc_as_pdf(drive_service, doc_file_id)
        file_id = upload_or_update_pdf(drive_service, pdf_stream, pdf_name, SHARED_DRIVE_FOLDER_ID)
        file_link = f"https://drive.google.com/file/d/{file_id}/view?usp=drive_link"
        for brd_item in brd_yml[brd_name]["current"]:
            if brd_item["name"] == "Product Sheet (PDF)":
                brd_item["url"] = file_link

    with open(BOARDS_FILE, 'w') as file:
        yaml.dump(brd_yml, file, default_flow_style=False)


if __name__ == '__main__':
    main()
