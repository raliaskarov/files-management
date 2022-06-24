#!/usr/bin/env python
#import exifread
import datetime
import hashlib
import os
import shutil
import subprocess

# config no trailing slashes please
source_path = input('Input source path: ')
destin_path = input('Input destination path: ')

# check if destination path is existing create if not
if not os.path.exists(destin_path):
    os.makedirs(destin_path)

print("file path check completed")

# file hash function
def hash_file(filename):

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

print(2)

#video date created function
def date_modified_info(path):
    # Read file
    open_file = open(path, 'rb')

    #get creation date and time data
    c_time = os.path.getmtime(path)
    #convert to datetime object
    creation_date_object = datetime.datetime.fromtimestamp(c_time)
    # Date and time
    year = str(creation_date_object.year)
    month = str(creation_date_object.month).zfill(2)
    day = str(creation_date_object.day).zfill(2)
    hour = str(creation_date_object.hour).zfill(2)
    minute = str(creation_date_object.minute).zfill(2)
    second = str(creation_date_object.second).zfill(2)

    #return date info in list
    output = [year, month, day, hour, minute, second, year + month + day + '-' + hour + minute + second]
    return output


print(2)

# get all picture files from directory and process
for file in os.listdir(source_path):
    filename = os.path.splitext(file)[0]
    ext = os.path.splitext(file)[1].lower()
    print(ext)
    if (ext == '.mov' or ext == '.mp4'):
        print("STRT!")
        filepath = source_path + os.sep + file
        dateinfo = date_modified_info(filepath)
        try:
            out_filepath = destin_path + os.sep + dateinfo[0] + os.sep + dateinfo[1]
            out_filename = out_filepath + os.sep + dateinfo[6] + ' ' + filename + ext
            print("output file name created: ", out_filename)

            # check if destination path is existing create if not
            if not os.path.exists(out_filepath):
                os.makedirs(out_filepath)
            print('Directory check completed')

            # copy the picture to the organised structure
            shutil.copy2(filepath,out_filename)
            print('file copied: ', out_filename)

            # verify if file is the same and display output
            if hash_file(filepath) == hash_file(out_filename):
                print ('File copied with success to  ', out_filename)
                os.remove(filepath)
                print('file removed: ', filepath)
            else:
                print ('File failed to copy :( ', filename)
            
        except:
            print ('error ', filename)
    else: print('different extension, going to next file')

print ("Done, freedom!")


# initate a scan
#subprocess.Popen("php /var/www/html/nextcloud/console.php files:scan --all", shell=True, stdout=subprocess.PIPE)