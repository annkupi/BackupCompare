import utils

def compare(first_backup_path, second_backup_path, target_backup_path):
    # debug
    for name in utils.all_filenames_in_path(first_backup_path):
        utils.extract_gz_content(name)

