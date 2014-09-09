#!/usr/bin/python

"""
Original script: Google Drive Quickstart in Python.
https://github.com/googledrive/python-quickstart
Install dependencies:
    sudo pip install --upgrade google-api-python-client
    sudo pip install unidecode
"""

#import pprint
import sys
import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client
import os
import webbrowser
from mimetypes import MimeTypes
import urllib
from unidecode import unidecode
from oauth2client.file import Storage

# OAuth 2.0 scope that will be authorized.
# Check https://developers.google.com/drive/scopes for all available scopes.
OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'

# Location of the client secrets.
CLIENT_SECRETS = 'client_secrets.json'

drive_service = None
folder_ids = {}

def authenticate():
    """
    Run the OAuth2.0 authorization flow and save credentials to local storage
    """
    global drive_service

    # Create a credential storage object.  You pick the filename.
    storage = Storage('my_credentials')

    # Attempt to load existing credentials.  Null is returned if it fails.
    credentials = storage.get()

    # Only attempt to get new credentials if the load failed.
    if not credentials:
        # Perform OAuth2.0 authorization flow.
        flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
        flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
        authorize_url = flow.step1_get_authorize_url()
        authorize_url = authorize_url + "&approval_prompt=force"
        print 'Go to the following link in your browser: ' + authorize_url
        webbrowser.open(authorize_url,new=2)
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
        #save the credentials for later use
        storage.put(credentials)
    # Create an authorized Drive API client.
    http = httplib2.Http()
    credentials.authorize(http)
    drive_service = apiclient.discovery.build('drive', 'v2', http=http)

def get_mime_type(file_path):
    """
    Return mime type of a file
    """
    if (unidecode(file_path) != file_path):
        return "application/octet-stream"
    mime = MimeTypes()
    url = urllib.pathname2url(file_path)
    mime_type = mime.guess_type(url)
    #print mime_type
    if mime_type[0]:
        return mime_type[0]
    else:
        return "application/octet-stream"

def upload_file(file_path, parent_id = None):
    """
    Upload one file
    """
    file_path = unicode(file_path)
    media_body = apiclient.http.MediaFileUpload(
        file_path,
        mimetype=get_mime_type(file_path),
        resumable=True
    )
    # The body contains the metadata for the file.
    path, filename = os.path.split(file_path)
    body = {
      'title': unidecode(filename),
      'description': '',
    }
    if parent_id:
        body['parents'] = [{'id': parent_id}]
    new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
    print("Uploaded " + file_path)

def get_dir_id(dir_path):
    if dir_path in folder_ids:
        return folder_ids[dir_path]
    else:
        return None

def get_dir_name(folder_path):
    path,folder_name = os.path.split(folder_path)
    return folder_name

def create_dir(dir_path, parent_id = None):
    """
    Create new directory in GDrive
    """
    dir_name = get_dir_name(dir_path)
    body = {
      'title': dir_name,
      'mimeType':"application/vnd.google-apps.folder"
    }
    if parent_id:
        body['parents'] = [{'id': parent_id}]
    new_dir = drive_service.files().insert(body=body).execute()
    folder_ids[dir_path] = new_dir['id']
    return new_dir['id']

def check_dir(path):
    """
    Walk through every files and directories within the input path
    to create directory in GDrive and upload file
    """
    #Important: must pass unicode path to os.walk to get file name as unicode string
    path = path.decode('utf-8')
    if os.path.isdir(path):
        #Upload everything within that input folder
        create_dir(path)
        for root, dirs, files in os.walk(path):
            parent_id = get_dir_id(root)
            for dir_name in dirs:
                create_dir(root + os.sep + dir_name, parent_id)
            for file_name in files:
                file_path = root + os.sep + file_name
                upload_file(file_path, parent_id)
    else:
        #Upload one input file
        upload_file(path)


def main():
    if len(sys.argv) == 1:
        print "Please provide the path to upload"
    else:
        authenticate()
        check_dir(sys.argv[1])
    pass

if __name__ == '__main__':
    main()