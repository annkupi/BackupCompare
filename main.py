import sys
sys.path.insert(0, "compare_tools")
import compare_backup

def main(args):
    if len(args) < 4:
        raise Exception('Not enough parameters')

    first_backup_path = args[1]
    second_backup_path = args[2]
    target_backup_path = args[3]

    compare_backup.compare(first_backup_path, second_backup_path, target_backup_path)

if __name__ == '__main__':
    main(sys.argv)