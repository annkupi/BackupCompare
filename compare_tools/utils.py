import gzip
import json
from os import walk

def all_filenames_in_path(path):
    for (dirpath, dirnames, filenames) in walk(path):
        names_with_path = [dirpath + '\\' + filename for filename in filenames]
        for item in names_with_path:
            yield item

def extract_gz_content(path):
    file = gzip.open(path, 'rb')
    file_content_dict = json.load(file)
    file.close()
    return file_content_dict