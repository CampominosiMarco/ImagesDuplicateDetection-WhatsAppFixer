import os
import hashlib
from image_analysis import *
from sys import argv
from colorama import Fore
import numpy as np

#   py -3 [-a/-f] [DIR] [FILE]
#   py -3 main.py
#   py -3 main.py -f .\path_test exif.png 

file_name = ""    #"reality.jpg"
mode = ""
dict_files = {}
array_files = np.empty((0,))    # 1 D, no elements
array_files_2_delete = np.empty((0,))
idx_counter = 1

#   argv check
if len(argv) == 4:
    mode = argv[1]
    directory = argv[2]
    file_name = argv[3].lower()
elif len(argv) == 3:
    mode = argv[1]
    if mode != "-a":
        print(Fore.RED + "For directory option, command must be '-a'" + Fore.RESET)
        quit()
    directory = argv[2]
else:
    mode = "-a"
    directory = os.getcwd()



#   Filter on extensions
def check_extension(file):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".gif"):
        return True
    else:
        return False



#   HASH code calculation
def calculate_sha256_hash(file_path):
    with open(file_path, "rb") as f:    #open file in binary mode
        content = f.read()
    sha256_hash = hashlib.sha256()      #SHA-256 algorithm
    sha256_hash.update(content)         #update with image content
    return sha256_hash.hexdigest()



#   Compare dictionaries
def compare_dictionaries(dict1, dict2):
    diff_dict1 = {}
    diff_dict2 = {}
    
    for key in dict1:
        if dict1.get(key) != dict2.get(key):
            diff_dict1[key] = dict1.get(key)
    
    for key in dict2:
        if dict2.get(key) != dict1.get(key):
            diff_dict2[key] = dict2.get(key)

    return diff_dict1, diff_dict2



#   Print dictionary informations
def print_dictionary(dict):
    if dict.items() == 0:
        print("\tNO DIFFERENCES.")
    else:
        for label,value in dict.items():
            print("\t" + f"{label:35}: {value}")



#   Business Logic
def analysis(dir, name):
    global array_files
    global dict_files
    global idx_counter
    global array_files_2_delete
    
    stringPath = dir  + "\\" + name
    uid = calculate_sha256_hash(stringPath)
    
    '''
    ALTERNATIVE:
        import time
        import pathlib
        import datetime
        
        fname = pathlib.Path(stringPath)
        mod_time = datetime.datetime.fromtimestamp(fname.stat().st_mtime).strftime("%d.%m.%Y %H:%M:%S")
        creation_time = datetime.datetime.fromtimestamp(fname.stat().st_ctime).strftime("%d.%m.%Y %H:%M:%S")

        #(NOT PREFERRED) unique ID with creation - modification - size
        uid = '%s%s%s%s%s' %(creation_time,'_',mod_time,'_',str(fname.stat().st_size))
        #(PREFERRED) unique ID with modification - size
        uid = '%s%s%s' %(mod_time,'_',str(fname.stat().st_size))
    '''
 
    if uid in array_files:
        array_files_2_delete = np.append(array_files_2_delete, stringPath)
        dict_KO = start_check(stringPath) #   Extract informations
        dict_OK = start_check(dict_files.get(uid))#   Extract informations
        first, second = compare_dictionaries(dict_KO, dict_OK)
        print (Fore.BLUE + "-"*50 + " [FILE TO DELETE", str(idx_counter) + "] " + "-"*50 + Fore.RED)
        print_dictionary(first)
        print (Fore.BLUE + "\t" + "*"*50 + " [UPPER FILE] " + "*"*50 + Fore.GREEN)
        print_dictionary(second)
        print (Fore.RESET + "-"*100)
        idx_counter = idx_counter + 1
    else:
        array_files = np.append(array_files, uid)
        dict_files[uid] = stringPath



#   Recoursive method to read all files in any directory
def list_directory(my_path, fileName = None):
    for file in os.listdir(my_path):
        if file == fileName:
         #   print("[", my_path , "]", file)
            analysis(my_path, file)

        filePath = my_path + "\\" + file
        if os.path.isdir(filePath):
            list_directory(filePath, fileName)
        else:
            if fileName == None and check_extension(file):
          #      print("[", my_path , "]", file)
                analysis(my_path, file)



if mode == "-a":
    list_directory(directory, None)
elif mode == "-f":
    list_directory(directory, file_name)
    
print("Files 2 delete:")
print(array_files_2_delete)