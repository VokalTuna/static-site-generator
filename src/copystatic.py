import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)
            copy_files(source_dir_path,dest_dir_path)

def copy_files(src,dest):
    files = os.listdir(src)
    for file in files:
        s = os.path.join(src,file)
        if not os.path.isfile(s):
            new_dest = os.path.join(dest,file)
            os.mkdir(new_dest)
            copy_files(s, new_dest)
        else:
            shutil.copy(s,dest)
