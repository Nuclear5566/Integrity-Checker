import sys
import hashlib
import os
import json
import copy

if len(sys.argv) < 3:
    print("Invalid Input")
    sys.exit(1)

functionCommand = sys.argv[1]
log_path = sys.argv[2]
json_dict = dict()
store_dir = "./"
store_path = store_dir + "output.json"

def is_dir(path): 
    if os.path.isfile(path):
        return False
    elif os.path.isdir(path):
        return True

def comp_hash(file_path, algorithim='sha256'): 
    hash_func = hashlib.new(algorithim)
    
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def write_init(hash, path): 
    json_dict.update({path: hash})

def loop_over_dir(): 
    if is_dir(log_path):
        for file in os.scandir(log_path):
            if file.is_file():
                file_path = file.path
                hash = comp_hash(file_path)
                write_init(hash, file_path)

def hash_file(): 
    if not is_dir(log_path):
        hash = comp_hash(log_path)
        write_init(hash, log_path)


def init(log_path):
    if os.path.exists(store_path) and os.path.isfile(store_path):
        if os.path.getsize(store_path):
            print("Initialization Failure: files already hashed")
            return
    if is_dir(log_path):
        loop_over_dir()
    elif not is_dir(log_path): 
        hash_file()
    with open(store_path, "a") as f:
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
    if not os.path.exists(store_path):
        print("Check Failure: no hashes to check")
        return
    else:
        with open(store_path, "r") as f:
            data = json.load(f)
        checkH(data)
   
def load_current_json():
    with open(store_path, "r") as f:
        temp_dict = json.load(f)
    return temp_dict

def update(log_path):
    if not os.path.exists(store_path):
        print("Update Failure: 'output.json' does not exist")
        return
    else:
        temp_dict = load_current_json()
        if is_dir(log_path):
            loop_over_dir()
        elif not is_dir(log_path):
            hash_file()
        new_dict = temp_dict | json_dict
        with open(store_path, "w") as f:
            json.dump(new_dict, f, indent = 4)
        print("Updated files successfully")

def main():
    if is_dir(log_path) == None:
        print("Invalid path")
        return
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