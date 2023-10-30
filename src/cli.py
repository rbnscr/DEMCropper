from .lib import *
import sys

def Main():
    # For CLI - tool
    print("Select path file.")
    path = path_from_file()
    print("Select xyz-files.")
    xyz_files = xyz_files_from_dialog()
    df_to_save = process_files_poly(path, xyz_files)
    if not df_to_save.empty:
        print("Select filename.")
        save_xyz(df_to_save)
    else:
        sys.exit()