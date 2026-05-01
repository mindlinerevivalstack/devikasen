import os
import dropbox
from dropbox.exceptions import ApiError

DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
DROPBOX_FOLDER = '/devikasen-photos'  # Your Dropbox folder path
LOCAL_FOLDER = 'images'

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

try:
    result = dbx.files_list_folder(DROPBOX_FOLDER)
    
    for entry in result.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            local_path = f"{LOCAL_FOLDER}/{entry.name}"
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            try:
                metadata, response = dbx.files_download(entry.path_display)
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {entry.name}")
            except ApiError as e:
                print(f"Error downloading {entry.name}: {e}")
except ApiError as e:
    print(f"Dropbox error: {e}")
