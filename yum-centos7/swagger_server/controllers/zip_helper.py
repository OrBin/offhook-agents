import subprocess
import os


def _create_parent_directory(output_file_path):
    dir_path = os.path.dirname(output_file_path)

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def compress_files(compressed_file_type, file_list, output_file_path, password=None):
    if compressed_file_type == '7z':
        seven_zip_command = ['7z', 'a']  # "Add to archive" command

        if password:
            seven_zip_command.append('-p' + password)

        seven_zip_command.extend([
            '-mhe=on',  # Enable archive header encryption (encrypt file list)
            '-sdel',  # Delete files after compression
            output_file_path
        ])

        seven_zip_command.extend(file_list)

        _create_parent_directory(output_file_path)
        subprocess.call(seven_zip_command)
    else:
        raise ValueError('Compressing to a %s file is not supported' % compressed_file_type)
