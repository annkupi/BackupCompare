import gzip
import json
import os


def all_filenames_in_path(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            yield dirpath, filename

def extract_gz_content(path):
    with gzip.open(path, 'rb') as f:
        file_content_dict = json.load(f)
    return file_content_dict

def save_json_to_gz(data, path, gz_filename):
    if not os.path.exists(path):
        os.makedirs(path)

    with gzip.open(path + '\\' + gz_filename, 'wb') as f:
        json.dump(data, f)
