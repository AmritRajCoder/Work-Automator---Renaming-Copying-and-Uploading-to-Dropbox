import os
import shutil
import dropbox

class Automate(object):
   def __init__(self, access_token, file_from, file_to_local, file_to_dropbox):
      self.access_token = access_token
      self.file_from = file_from
      self.file_to_local = file_to_local
      self.file_to_dropbox = file_to_dropbox
   def rename(self, base_name, extension):
      lst_file = os.listdir(self.file_from)
      cnt=1

      for file in lst_file:
         name, ext = os.path.splitext(file)
         ext=ext[1:]
         if ext==extension:
            fname = base_name + str(cnt) + "." +extension
            os.rename((self.file_from + "/" + file), (self.file_from + "/" + fname))
            cnt=cnt+1
      print("Files Renamed!")

   def moveLocal(self):
      lst = os.listdir(self.file_from)
      for file in lst:
         name, ext = os.path.splitext(file)
         ext = ext[1:]
         if ext == "":
            continue
         if os.path.exists(self.file_to_local + "/" + ext):
            shutil.copy((self.file_from + "/" + file), (self.file_to_local + "/" + ext + "/" + file))
         else:
            os.mkdir(self.file_to_local + "/" + ext)
            shutil.copy((self.file_from + "/" + file), (self.file_to_local + "/" + ext + "/" + file))
      print("Files Copied!")
      
   def uploadFiles(self):
      dbx = dropbox.Dropbox(self.access_token)
      lst = os.listdir(self.file_from)
      for file in lst:
         with open((self.file_from+"/" + file), 'rb') as f:
            dbx.files_upload(f.read(), (self.file_to_dropbox+file))
      print("Files Uploaded!")

def main():
   tok = input("Enter access token: ")
   f_fro = input("Enter path of the folder you wish to automate: ")
   f_to_loc = input("Enter path of folder where you would like to copy all files: ")
   f_to_drop = input("Enter path in dropbox where you would like to upload the contents: ")
   obj = Automate(tok, f_fro, f_to_loc, f_to_drop)
   ren = input("Would you like to rename your files? (Y/N) ")
   if ren=="Y":
      bname = input("Enter base name to be followed in every file: ")
      e = input("Enter the extension of the type of files you would like to rename: ")
      obj.rename(bname, e)
   m = input("Would you like to copy your files to the folder address you entered earlier? (Y/N) ")
   if m=="Y":
      obj.moveLocal()
   d=input("Would you like to upload your files to dropbox? (Y/N) ")
   if d=="Y":
      obj.uploadFiles()
   print("Thank You!")

main()