from googleapiclient.discovery import build
import yaml

from drive_utils import authenticate, download_doc_as_pdf, upload_or_update_pdf

BOARDS_FILE = './_data/board.yml'
SHARED_DRIVE_FOLDER_ID = '14hBAGJ9ni-QwqH_7yAbrO45Yd_k_baxA'

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
    "hdsocv1_evalr2": {
        "id": "14J4TGflgIARMwrq3gnrOdwsDA3Yf9PRbpP4T9eq8dOY",
        "name": "HDSOCv1 Eval Rev3 Quick Start Guide",
    }
}


def main():
    """Export Quick Start Guide Google Docs as PDFs, upload to shared Drive, and update board.yml URLs."""
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
            if brd_item["name"] == "Quick Start Guide (PDF)":
                brd_item["url"] = file_link

    with open(BOARDS_FILE, 'w') as file:
        yaml.dump(brd_yml, file, default_flow_style=False)


if __name__ == '__main__':
    main()
