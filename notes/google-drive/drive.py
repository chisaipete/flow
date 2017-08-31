from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
file_list = drive.ListFile({'q':"'root' in parent and trashed=false"}).GetLIst()
for f in file_list:
    print('title: {}, id: {}'.format(f['title'], f['id']))