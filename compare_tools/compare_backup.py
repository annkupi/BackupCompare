import utils

def compare_content(data1, data2):
    deleted = []
    created = []
    changed = []

    id_dict1 = {item['id']: item for item in data1}
    id_dict2 = {item['id']: item for item in data2}

    ids1 = set(id_dict1.keys())
    ids2 = set(id_dict2.keys())

    deleted_ids = ids1.difference(ids2)
    created_ids = ids2.difference(ids1)
    other_ids = ids1.intersection(ids2)

    for id in deleted_ids:
        deleted.append({
            'id': id,
            'userType': id_dict1[id].get('userType')
        })

    for id in created_ids:
        created.append({
            'id': id,
            'userType': id_dict1[id].get('userType')
        })

    for id in other_ids:
        for key, value in id_dict1[id].items():
            if value != id_dict2[id].get(key):
                changed.append({
                    "id": id,
                    "attribute": key,
                    "oldValue": value,
                    "newValue": id_dict2[id].get(key)
                })

    return {
        "Deleted": deleted,
        "Added": created,
        "ChangedAttribute": changed
    }

def save_diff(diff, path, subpath, gz_filename):
    if subpath:
        path += '\\' + subpath
    utils.save_json_to_gz(diff, path, gz_filename, 'change.json')

def compare(first_backup_path, second_backup_path, target_backup_path):
    # debug
    first_filenames=utils.all_filenames_in_path(first_backup_path)
    second_filenames=utils.all_filenames_in_path(second_backup_path)
    for first_subpath, first_filename in first_filenames:
        second_subpath, second_filename = next(second_filenames)

        #debug, delete
        print(first_filename)
        print(second_filename)

        first_content = utils.extract_gz_content(
            utils.make_full_path(first_backup_path, first_subpath, first_filename)).get('value')
        second_content = utils.extract_gz_content(
            utils.make_full_path(second_backup_path, second_subpath, second_filename)).get('value')

        diff = compare_content(first_content, second_content)
        save_diff(diff, target_backup_path, first_subpath, first_filename)
