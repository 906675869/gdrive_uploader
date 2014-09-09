GDrive Uploader
===============

Simple Google Drive uploader in Python 
(based on the quick start script at https://github.com/googledrive/python-quickstart)

####1) Install dependencies:
```
  sudo pip install --upgrade google-api-python-client
  sudo pip install unidecode
```
####2) Change Google Drive Client Secret (optional):
Replace client_secrets.json with your own json file downloaded from Google API Console (native application).

####3) Usage:
```
python gdrive_upload.py [directory or file to upload]
```
