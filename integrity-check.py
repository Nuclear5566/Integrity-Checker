import sys
import hashlib
import os
import json
import copy

functionCommand = sys.argv[1]
log_path = sys.argv[2]
json_dict = dict()

def is_dir(path): #checks if input is a file or directory
    if os.path.isfile(path):
        return False
    elif os.path.isdir(path):
        return True

def comp_hash(file_path, algorithim='sha256'): #calculates hash for a file
    hash_func = hashlib.new(algorithim)
    
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def write_init(hash, path): #stores hashes in a dictionary
    json_dict.update({path: hash})

def loop_over_dir(): #loops over a directory, hashes and stores
    if is_dir(log_path):
        for file in os.scandir(log_path):
            if file.is_file():
                file_path = file.path
                hash = comp_hash(file_path)
                write_init(hash, file_path)

def hash_file(): #hashes one file
    if not is_dir(log_path):
        hash = comp_hash(log_path)
        write_init(hash, log_path)


def init(log_path):
    if os.path.exists("./output.json") and os.path.isfile("./output.json"):
        if os.path.getsize("./output.json"):
            print("Initialization Failure: files already hashed")
            return
    if is_dir(log_path):
        loop_over_dir()
    elif not is_dir(log_path): 
        hash_file()
    with open("output.json", "a") as f:
        json.dump(json_dict, f, indent = 4)
    print("Hashes stored successfully")

def rehash_check(log_path):
    if is_dir(log_path):
        loop_over_dir()
    elif not is_dir(log_path):
        hash_file()
    new_dict = copy.deepcopy(json_dict)
    json_dict.clear()
    return new_dict

def search_modified(temp_dict, file_dict):
    mismatch = []
    for key in file_dict:
        if key in temp_dict and key in file_dict:
            if not file_dict[key] == temp_dict[key]:
                mismatch.append(key)
    return mismatch

def search_new(temp_dict, file_dict):
    new_entries = dict()
    for key in temp_dict:
        if key not in file_dict:
            new_entries[key] = temp_dict[key]
    return new_entries

def search_missing(temp_dict, file_dict):
    missing_entries = dict()
    for key in file_dict:
        if key not in temp_dict:
            missing_entries[key] = file_dict[key]
    return missing_entries

def check_unmodified(temp_dict, file_dict):
    if len(temp_dict) != len(file_dict):
        return False
    for key in temp_dict:
        if key not in temp_dict:
            return False
        if key not in file_dict:
            return False
        if temp_dict[key] != file_dict[key]:
            return False
    return True
def checkH(file_dict):
    temp_dict = rehash_check(log_path)
    checked = check_unmodified(temp_dict, file_dict)
    if checked:
        print("Unmodified")
    if len(file_dict) < len(temp_dict):
        print("New files detected, please run 'update'")
        temp = search_new(temp_dict, file_dict)
        print("New Files: \n")
        print(temp)
    if len(file_dict) > len(temp_dict):
        print("Missing files, please run 'update'")
        temp = search_missing(temp_dict, file_dict)
        print("Missing Files: \n")
        print(temp)
    modified_list = search_modified(temp_dict, file_dict)
    if not len(modified_list) == 0:
        print("Modified")
        print(modified_list)

def check(log_path):
    if not os.path.exists("./output.json"):
        print("Check Failure: no hashes to check")
        return
    else:
        with open("./output.json", "r") as f:
            data = json.load(f)
        checkH(data)
   
def update(log_path):
    if not os.path.exists("./output.json"): 
        print("Update Failure: 'output.json' does not exist")
        return
    with open("output.json", "r") as f:
        json_dict = json.load(f)
    
        

def main():
    if functionCommand.lower() == 'init':
        init(log_path)
    elif functionCommand.lower() == 'check':
        check(log_path)
    elif functionCommand.lower() == 'update':
        update(log_path)
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()