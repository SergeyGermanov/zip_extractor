# importing required modules
import os
from zipfile import ZipFile

file_number_extracted = 0
file_number = 0
folder_number = 0

# # specifying the zip file name
# file_name = "my_python_files.zip"

# go through the list of files
for file in os.listdir():

    # if it is a folder do not read
    if os.path.isdir(file):
        continue
    # opening the zip file in READ mode

    if file.endswith('.zip'):

        folder_name = os.path.splitext(file)[0]
        folder_in = os.getcwd()
        path = os.path.join(folder_in, folder_name)

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print("New Folder has been created: " + folder_name)
            folder_number += 1

        with ZipFile(file, 'r') as zip:
            # printing all the contents of the zip file
            # zip.printdir()
            all_files = zip.namelist()

            print('Extracting now to: ' + folder_name)

            for name in all_files:
                print('Extracting file: ' + name)
                file_number_extracted += 1

            print(path)
            # extracting all the files
            zip.extractall(u'\\\\?\\' + path)

            print('Done with file - ' + file)
            file_number += 1

print("UnZipping Completed!")
print("Total number of folders created: " + str(folder_number))
print("Total number of Zip files processed: " + str(file_number))
print("Total number of files extracted: " + str(file_number_extracted))