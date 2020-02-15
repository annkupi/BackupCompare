import gzip
import json
import os
import shutil

def all_filenames_in_path(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            yield dirpath[len(path) + 1:], filename

def make_full_path(path, subpath, file_name):
    return '{}\\{}\\{}'.format(path, subpath, file_name)

def extract_gz_content(path):
    with gzip.open(path, 'rb') as f:
        file_content_dict = json.load(f)
    return file_content_dict

def save_json_to_gz(data, path, gz_filename, filename):
    if not os.path.exists(path):
        os.makedirs(path)

    internal = open(path + '\\' + filename, 'wb')
    json.dump(data, internal)
    internal.close()
    internal = open(path + '\\' + filename, 'rb')
    with gzip.open(path + '\\' + gz_filename, 'wb') as f:
        shutil.copyfileobj(internal, f)
    internal.close()
    os.remove(path + '\\' + filename)