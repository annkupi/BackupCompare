import utils


class BackupComparer(object):
    def __init__(self, first_backup_path, second_backup_path, target_path):
        self.paths = {
            'first': first_backup_path,
            'second': second_backup_path,
            'target': target_path
        }

        self.all_ids = {
            'first': set(),
            'second': set()
        }

        self.deleted_ids = None
        self.created_ids = None
        self.other_ids = None

        self.changes = {
            'Deleted': [],
            'Added': [],
            'ChangedAttribute': []
        }

    def compare_and_save(self):
        self.record_all_ids('first')
        self.record_all_ids('second')
        self.record_ids_by_categories()

        self.process_deleted_ids()
        self.process_created_ids()
        self.process_other_ids()

        self.save_formatted_diff()

    def all_datasets(self, number):
        filenames = utils.all_filenames_in_path(self.paths[number])
        for dirpath, filename in filenames:
            yield utils.extract_gz_content('{}\\{}'.format(dirpath, filename)).get('value')

    def record_all_ids(self, number):
        for dataset in self.all_datasets(number):
            self.add_ids_from_data(dataset, number)

    def add_ids_from_data(self, data, number):
        for item in data:
            self.all_ids[number].add(item['id'])

    def record_ids_by_categories(self):
        self.deleted_ids = self.all_ids['first'].difference(self.all_ids['second'])
        self.created_ids = self.all_ids['second'].difference(self.all_ids['first'])
        self.other_ids = self.all_ids['first'].intersection(self.all_ids['second'])

    def process_deleted_ids(self):
        if not self.deleted_ids:
            return

        for dataset in self.all_datasets('first'):
            for user in dataset:
                if user.get('id') in self.deleted_ids:
                    self.changes['Deleted'].append({
                        'id': user.get('id'),
                        'userType': user.get('userType')
                    })

    def process_created_ids(self):
        if not self.created_ids:
            return

        for dataset in self.all_datasets('second'):
            for user in dataset:
                if user.get('id') in self.created_ids:
                    self.changes['Added'].append({
                        'id': user.get('id'),
                        'userType': user.get('userType')
                    })

    def process_other_ids(self):
        if not self.other_ids:
            return

        for first_dataset in self.all_datasets('first'):
            first_id_dict = self.get_id_dict_from_dataset(first_dataset, self.other_ids)
            for second_dataset in self.all_datasets('second'):
                second_id_dict = self.get_id_dict_from_dataset(second_dataset, self.other_ids)
                for id in self.other_ids:
                    if id in first_id_dict and id in second_id_dict:
                        self.changes['ChangedAttribute'].extend(self.compare_attributes(id, first_id_dict[id], second_id_dict[id]))

    def get_id_dict_from_dataset(self, dataset, acceptable_ids=None):
        result = {}
        for item in dataset:
            if acceptable_ids and item.get('id') in acceptable_ids:
                result[item.get('id')] = item

        return result

    def compare_attributes(self, id, attrs1, attrs2):
        result = []

        for key, value1 in attrs1.items():
            if key not in attrs2:
                result.append({
                    "id": id,
                    "attribute": key,
                    "oldValue": value1,
                    "newValue": None
                })
            elif value1 != attrs2[key]:
                result.append({
                    "id": id,
                    "attribute": key,
                    "oldValue": value1,
                    "newValue": attrs2[key]
                })

        for key, value in attrs2.items():
            if key not in attrs1:
                result.append({
                    "id": id,
                    "attribute": key,
                    "oldValue": None,
                    "newValue": value
                })

        return result

    def save_formatted_diff(self):
        utils.save_json_to_gz(self.changes, self.paths['target'], 'change.gz')


def compare(first_backup_path, second_backup_path, target_backup_path):
    comparer = BackupComparer(first_backup_path, second_backup_path, target_backup_path)
    comparer.compare_and_save()
