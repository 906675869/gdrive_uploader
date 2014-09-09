GDrive Uploader
===============

Google Drive uploader in Python
(based on the quick start script at https://github.com/googledrive/python-quickstart)

**Features:**
* Upload all files and subdirectories within the input path
* Store credentials on the computer, which means you only need to authorize it once
* Sanitize special characters (using unidecode)

####1) Install dependencies:
```
  sudo pip install --upgrade google-api-python-client
  sudo pip install unidecode
```
####2) Change Google Drive Client Secret (optional):
Replace client_secrets.json with your own json file downloaded from Google API Console (native application).

####3) Usage:
```
python gdrive_upload.py [directory or file path to be uploaded]
```
When the Permission page pops up in your browser, hit "Accept", copy the verification code and paste it back into the command line.
