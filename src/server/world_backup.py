import os
import shutil
import zipfile
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Set the server directory and backup directory paths
server_dir = "/path/to/minecraft/server/directory"
backup_dir = "/path/to/minecraft/server/backup/directory"

# Set the Google Drive credentials file path
gauth_path = "/path/to/google/drive/credentials.json"

# Set the Google Drive backup folder ID
backup_folder_id = "google_drive_folder_id"

# Get the current date and time
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create the backup directory if it doesn't exist
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Archive the server world directory
backup_file = os.path.join(backup_dir, f"world_{timestamp}.zip")
shutil.make_archive(backup_file[:-4], "zip", server_dir)

# Upload the backup file to Google Drive
gauth = GoogleAuth()
gauth.LoadCredentialsFile(gauth_path)
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile(gauth_path)

drive = GoogleDrive(gauth)
file_metadata = {"title": os.path.basename(backup_file), "parents": [{"id": backup_folder_id}]}
file = drive.CreateFile(file_metadata)
file.SetContentFile(backup_file)
file.Upload()

# Clean up old backup files (keep only the 24 most recent backups)
backup_files = os.listdir(backup_dir)
backup_files.sort()
while len(backup_files) > 24:
    old_backup_file = os.path.join(backup_dir, backup_files.pop(0))
    os.remove(old_backup_file)
