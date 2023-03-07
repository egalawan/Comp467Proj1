import os
import time

d_Path = 'week3'  # set the folder path to the current directory
files_Set = set()

while True:
    # get the list of files in the directory
    files_set = set(os.listdir(d_Path))

    # get the set of new files (i.e., files that were not previously known)
    new_Files_Set = files_set - files_Set

    # iterate over the new files
    for new_File_Name in new_Files_Set:
        new_File_Path = os.path.join(d_Path, new_File_Name)

        # check if the file is a regular file (i.e., not a directory)
        if os.path.isfile(new_File_Path):
            # get the file type
            file_Type = os.path.splitext(new_File_Name)[-1]
            # get the file creation time
            creation_Time = os.path.getctime(new_File_Path)
            if not file_Type:
                file_Type = 'txt'

            

            # report back to the user
            print(f'New file found: {new_File_Name}')
            print(f'Type of file: {file_Type}')
            print(f'Creation time: {time.ctime(creation_Time)}')

    # Update the known files set
    files_Set = files_set

    # wait for 1 second before checking again
    time.sleep(1)
