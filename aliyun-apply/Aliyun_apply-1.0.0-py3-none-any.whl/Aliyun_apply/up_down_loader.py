import aligo
import os
ali = aligo.Aligo()

def clean_cloud_folder(folder_id):
    exist_info = ali.get_file_list(folder_id)
    print('已存在文件:',[i.name for i in exist_info])
    for fobj in exist_info:
        ali.move_file_to_trash(fobj.file_id)

def uploader(foldid,filelist):
    clean_cloud_folder(foldid)
    for f in filelist:
        ali.upload_file(f,foldid)

def downloader(sourcefolderid,downloadfiles,targetfolder):
    filelist = os.listdir(targetfolder)
    for f in downloadfiles:
        if f in filelist:
            os.remove(targetfolder+f)
    exist_info = ali.get_file_list(sourcefolderid)
    for f in exist_info:
        if f.name in downloadfiles:
            ali.download_file(file = f,local_folder = targetfolder)   
    