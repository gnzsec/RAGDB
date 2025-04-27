import os.path
import pickle
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_FILE = '../credentials/google_credentials.json' # Adjust path as needed
TOKEN_FILE = '../credentials/token.pickle' # Adjust path as needed

def get_drive_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Ensure the credentials file exists
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"Error: Credentials file not found at {os.path.abspath(CREDENTIALS_FILE)}")
                print("Please download your Google Cloud API credentials (OAuth 2.0 Client ID)")
                print("and save them as 'google_credentials.json' in the 'credentials' directory.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('drive', 'v3', credentials=creds)
        print("Successfully connected to Google Drive API.")
        return service
    except HttpError as error:
        print(f'An error occurred connecting to Google Drive API: {error}')
        return None
    except Exception as e:
        print(f"An unexpected error occurred during authentication: {e}")
        # Attempt to delete potentially corrupted token file
        if os.path.exists(TOKEN_FILE):
            try:
                os.remove(TOKEN_FILE)
                print(f"Deleted potentially corrupted token file: {TOKEN_FILE}. Please try running the script again.")
            except OSError as oe:
                print(f"Error deleting token file {TOKEN_FILE}: {oe}")
        return None


def list_files(service, folder_id=None, page_size=10):
    """Lists files in Google Drive, optionally filtering by folder."""
    try:
        query = None
        if folder_id:
            query = f"'{folder_id}' in parents"

        results = service.files().list(
            pageSize=page_size,
            q=query,
            fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return []
        print('Files:')
        for item in items:
            print(f"- {item['name']} ({item['id']}) - Type: {item.get('mimeType', 'N/A')}")
        return items
    except HttpError as error:
        print(f'An error occurred listing files: {error}')
        return []
    except Exception as e:
        print(f"An unexpected error occurred while listing files: {e}")
        return []

def download_file(service, file_id, file_name, download_path="../data/downloaded_files"):
    """Downloads a file from Google Drive."""
    try:
        # Ensure the download directory exists
        os.makedirs(download_path, exist_ok=True)

        request = service.files().get_media(fileId=file_id)
        # Use io.BytesIO to handle the downloaded content in memory
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print(f"Downloading file: {file_name} ({file_id})...")
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download {int(status.progress() * 100)}%.")

        # Once download is complete, write the BytesIO content to a file
        file_path = os.path.join(download_path, file_name)
        with open(file_path, "wb") as f:
            f.write(fh.getvalue())

        print(f"File '{file_name}' downloaded successfully to {os.path.abspath(file_path)}")
        return file_path

    except HttpError as error:
        print(f'An error occurred downloading file {file_id}: {error}')
        return None
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        return None

# Example usage (optional, can be run directly for testing)
if __name__ == '__main__':
    drive_service = get_drive_service()
    if drive_service:
        # Replace 'YOUR_FOLDER_ID' with the actual ID of the folder you want to monitor
        # You can find the ID in the URL of the folder in Google Drive
        # e.g., https://drive.google.com/drive/folders/THIS_IS_THE_ID
        target_folder_id = None # Set to None to list root files, or provide ID
        files_to_download = list_files(drive_service, folder_id=target_folder_id, page_size=5) # Limit for testing

        # --- Example Download --- 
        # Uncomment and set a file ID and name from the list above to test download
        # test_file_id = 'REPLACE_WITH_A_FILE_ID_FROM_LIST'
        # test_file_name = 'REPLACE_WITH_CORRESPONDING_FILE_NAME'
        # if test_file_id != 'REPLACE_WITH_A_FILE_ID_FROM_LIST':
        #     download_file(drive_service, test_file_id, test_file_name)
        # else:
        #     print("\nPlease set test_file_id and test_file_name in the script to test download.")


# --- TODO ---
# Function to periodically check for new files in the target folder 