import sys
import hashlib
import os
import json
import argparse

functionCommand = sys.argv[1]
log_path = sys.argv[2]
json_dict = dict()

'''
def fileGrabber():
    with open(log_path, 'a+') as openedFile:
        openedFile.seek(0)
        file = openedFile.read()
        return file
'''

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
    #temp_json_dict = json_dict
    print("Hashes stored successfully")

def main():
    if functionCommand.lower() == 'init':
        init(log_path)
    elif functionCommand.lower() == 'check':
        temp = 0
    elif functionCommand.lower() == 'update':
        temp = 0
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()