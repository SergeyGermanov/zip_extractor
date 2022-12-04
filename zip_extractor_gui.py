# zip_extractor.py

import PySimpleGUI as sg
import os
from zipfile import ZipFile

# First the window layout in 2 columns
folder_from = ''
folder_to = ''
unzip_list = ''


def extract_function(folder_from, folder_to):
    file_number_extracted = 0
    file_number = 0
    folder_number = 0

    if (folder_from != '' or folder_to != ''):

        os.chdir(folder_from)

        # go through the list of files
        for file in os.listdir():

            # if it is a folder do not read
            if os.path.isdir(file):
                continue
            # opening the zip file in READ mode

            if file.endswith('.zip'):

                folder_name = os.path.splitext(file)[0]
                folder_in = folder_to
                path = os.path.join(folder_in, folder_name)

                os.chdir(folder_to)

                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)

                    window["-TOUT-"].update(
                        "New Folder has been created: " + folder_name)
                    file_list = os.listdir(folder_in)
                    window["-UNZIP FILE LIST-"].update(file_list)
                    window["-FOLDER CRT-"].update("Total number of folders created: " +
                                                  str(folder_number))
                    window.refresh()

                    folder_number += 1

                os.chdir(folder_from)

                with ZipFile(file, 'r') as zip:
                    # printing all the contents of the zip file
                    # zip.printdir()
                    all_files = zip.namelist()

                    window["-TOUT-"].update('Extracting now to: ' +
                                            folder_name)
                    window.refresh()

                    for name in all_files:

                        # beautiful look percentage - start

                        # uncompress_size = sum(
                        #     (file.file_size for file in name.infolist()))

                        # extracted_size = 0

                        # for file in name.infolist():
                        #     extracted_size += file.file_size
                        #     print("%s %%\r" %
                        #           (extracted_size * 100/uncompress_size))

                        # beautiful look percentage - end

                        window["-TOUT-"].update('Extracting file: ' + name)
                        window["-EXTRACTED-"].update("Total number of files extracted: " +
                                                     str(file_number_extracted))
                        window.refresh()
                        file_number_extracted += 1

                    # extracting all the files
                    zip.extractall(u'\\\\?\\' + path)

                    window["-TOUT-"].update('Done with file - ' + file)
                    window["-ZIP-"].update("Total number of Zip files processed: " +
                                           str(file_number))
                    window.refresh()
                    file_number += 1

        window["-TOUT-"].update('UnZipping Completed!')
        window["-FOLDER CRT-"].update("Total number of folders created: " +
                                      str(folder_number))
        window["-ZIP-"].update("Total number of Zip files processed: " +
                               str(file_number))
        window["-EXTRACTED-"].update("Total number of files extracted: " +
                                     str(file_number_extracted))

        # print("Total number of folders created: " + str(folder_number))
        # print("Total number of Zip files processed: " + str(file_number))
        # print("Total number of files extracted: " + str(file_number_extracted))
    else:
        sg.popup('You need to choose the folder to and from!')


file_list_column = [
    [
        sg.Text("Folder From"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
second_column = [
    [
        sg.Text("Folder To"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER TO-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-UNZIP FILE LIST-"
        )
    ],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(second_column),
    ],
    [sg.HSeparator()],
    [
        sg.Text('Lets start!', size=(40, 1), key="-TOUT-")
    ],
    [
        sg.Text("Total number of folders created: 0",
                size=(40, 1), key="-FOLDER CRT-")
    ],
    [
        sg.Text("Total number of Zip files processed: 0",
                size=(40, 1), key="-ZIP-")
    ],
    [
        sg.Text("Total number of files extracted: 0",
                size=(40, 1), key="-EXTRACTED-")
    ],
    [sg.HSeparator()],
    [sg.Button('Extract All')]

]

window = sg.Window("Zip Extractor", layout)

# Run the Event Loop
while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder_from = values["-FOLDER-"]

        try:
            # Get list of files in folder
            file_list = os.listdir(folder_from)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder_from, f))
            and f.lower().endswith((".zip"))
        ]
        window["-FILE LIST-"].update(fnames)

# second column
    if event == "-FOLDER TO-":
        folder_to = values["-FOLDER TO-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder_to)
        except:
            file_list = []

        window["-UNZIP FILE LIST-"].update(file_list)

# button to extract all function
    if event == 'Extract All':
        extract_function(folder_from, folder_to)

window.close()
