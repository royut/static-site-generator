import os
import shutil


def copy_files(source, destination):
    shutil.rmtree(destination)
    copy_files_recursive(source, destination)
    return

def copy_files_recursive(source, destination):
    if not os.path.exists(source):
        raise Exception(f'Source: {source} does not exist')
    if not os.path.exists(destination):
        if not os.path.isfile(source):
            os.mkdir(destination)
    if os.path.isfile(source):
        shutil.copy(source, destination)
        return
    else:
        for path in os.listdir(source):
            copy_files_recursive(os.path.join(source, path), os.path.join(destination, path))