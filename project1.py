
import argparse
import csv
from itertools import product
import sys

#Don Thisura Nawalage
"""

#computation done to match shareholder's request
    #replace file system from local baselight to facility
    #storage(remember color correcter's prefer local storage for bandwidth issues)
    #don't forget about the <err> ones, ignore put as null?

    #Each work order is gonna be different
"""

#argparse uses the command line to find the location of the txt file we wanna parse
parser = argparse.ArgumentParser()
#now we want to add what the argument is gonna be #we are doing it like this because the file isn't always gonna have
#the same name and location, nargs * = 0 or more files, + = 1 or more
parser.add_argument('file', nargs= '+', help = "Need to add path to Workorder txt")

#parsing the command line 
args = parser.parse_args()

#Baselight_export.txt file
with open(args.file[1], "r") as file1:
    Locations = []
    final_Folder = ''
    newLoc = ''
    lines = file1.readlines()
    for row in lines:
        new_Row = row.replace('<err>', "").replace('<null>', "")
        if '/images1/' in new_Row:
            final_Folder = new_Row.split("/images1/")[1].split("/")[0]
        #final folder is 'starwars' idk why i did that but i did
        if final_Folder in new_Row:
            #gets each of the baselight_export lines from this line on
            Locations.append(new_Row.strip().split())
        

#parse data
#Xytech file to get the job description
with open(args.file[0], "r") as file:
    work_Order = file.readline().strip()
    #print(work_Order)
    lines = file.read()
    work_Locations = []
    #needed to do the index stuff to save the locations of each of the lines
    #the producer
    if 'Producer:' in lines:
        start_index = lines.find('Producer:') + len('Producer: ')
        end_index = lines.find('\n', start_index)
        #-1 gets the last time producer is mentioned
        work_Producer = lines[start_index:end_index].strip()
    #the operator
    if 'Operator:' in lines:
        start_index = lines.find('Operator:') + len('Operator: ')
        end_index = lines.find('\n', start_index)
        #-1 gets the last time producer is mentioned
        work_Operator = lines[start_index:end_index].strip()
    #the job needed to be done
    if 'Job:' in lines:
        start_index = lines.find('Job:') + len('Job: ')
        end_index = lines.find('\n', start_index)
        #-1 gets the last time producer is mentioned
        work_Job_Description = lines[start_index:end_index].strip()

    #notes 
    if 'Notes:' in lines:
        # Extract the Notes field
        start_index = lines.find('Notes:') + len('Notes:')
        end_index = len(lines)
        #if notes are longer than just one line
        work_Notes = lines[start_index:end_index].strip()
    
    #need to use the location and see what is same as baselight #it is in a different directory but starwars is the same #Location: /hpsans13/production/starwars/reel1/partA/1920x1080
    # Extract the Locations field
    if 'Location:' in lines:
        start_index = lines.find('Location:') + len('Location:')
        #len("Location:") gives 9 spaces to save those spaces
        #need to double indent to see where the empty space is because at each line there is a \n but at the end there \n\n
        end_index = lines.find('\n\n', start_index)
        #to get all the locations
        #split indicates where to go to next string so it changes to another string after indent
        locations = lines[start_index:end_index].strip("\n").split()
        work_Locations.append(locations)
#for the folders after starwars
work_folders = []
dont_need = {"/hpsans13/production" : "", "/hpsans12/production" : "", "/hpsans14/production" : "", "/hpsans15/production" : "" }
for location in work_Locations:
    folder = []
    for path in location:
        if "/starwars/" in path:
            folder.append("/".join(path.split("/production/")[-1:]))
        else:
            for item in dont_need:
                path = path.replace(item, "")
            folder.append(path)
    work_folders.append(folder)

#Trying to see if starwars from Xytech is in the baselight
#print(final_Folder)
start_Process = False

for locations in work_folders:
    for lines in locations:
        if final_Folder in lines:
            start_Process = True

#if the folder is found inside the other folder then start the process of switching
if start_Process == True:
   #so now each request is separated with []
    #work_folder is the folder from XYtech with the workorder all the orders
    #element = = [starwars/reel..]

    # create a dictionary to hold the total numbers for each order
    Final_Order = {}
   
    found = False

    #attaching the workorder to the number from the other files
    # iterate through the work_folders list
    #print(work_folders)
    for orders in work_folders:
        #iterate through each order in the orders list
        for order in orders:
            #print(order)
            #iterate through the Locations list
            for location in Locations:
            #    print("----")
            #    print(order)
            #    print(location[0])
            #    print("----")
               if order in location[0]:
                   found = True
                   all_locations = location[1:]
                   if order in Final_Order:
                        Final_Order[order].extend(all_locations)
                   else:
                        Final_Order[order] = all_locations
            if not found:
                found = False
##final_order is the directory
###fixing the dictionary so that the ranges work accoring to how close they are to eachother

Final = False

for key in Final_Order:
    value = Final_Order[key]
    range_list = []
    start_num = None
    end_num = None
    for num in sorted(value, key=int):
        if start_num is None:
            start_num = int(num)
            end_num = int(num)
        elif int(num) == end_num + 1:
            end_num = int(num)
        else:
            if start_num == end_num:
                range_list.append(str(start_num))
            else:
                range_list.append(f"{start_num}-{end_num}")
            start_num = int(num)
            end_num = int(num)
    if start_num is not None:
        if start_num == end_num:
            range_list.append(str(start_num))
        else:
            range_list.append(f"{start_num}-{end_num}")
    Final_Order[key] = range_list
    Final = True
# create a new dictionary to hold the updated ranges

if Final == True:
    found = False
    #attaching the workorder to the number from the other files
    # iterate through the work_folders list


# print the final dictionary with grouped ranges
# print the final dictionary with grouped ranges
for loc in work_Locations[0]:    
    for key, value in Final_Order.items():
        if key in loc:
            Final_Order[loc] = value
            del Final_Order[key]
            break
    print(f"{loc}: {', '.join(value)}")


with open("Project1.csv", "w", newline="") as csvfile:
    fields = ["Producer: ", "Operator: ", "Job: ", "Notes: "]
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerow({"Producer: ": work_Producer, "Operator: ": work_Operator, "Job: ": work_Job_Description, "Notes: ": work_Notes})
    Write = csv.writer(csvfile)
    Write.writerow(["File", "Data"])
    for key, value in Final_Order.items():
        Write.writerow([key, value])