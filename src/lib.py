import warnings


import pandas as pd
from alive_progress import alive_bar
import numpy as np

import tkinter.filedialog as fd

from matplotlib.path import Path


warnings.simplefilter(action='ignore', category=FutureWarning)

def process_files_poly(target_path: list, xyz_files: list):

    p = Path(target_path)
    df_all = pd.DataFrame(columns=["x", "y", "z"])
    with alive_bar(len(xyz_files),dual_line=True) as bar:
        for file in xyz_files:
            bar.text = f"-> Processing file: {file}, please wait..."
            df = pd.read_table(
                file, delim_whitespace=True, header=None, names=["x", "y", "z"]
            )
            contained_points = p.contains_points(df.to_numpy()[:,:2])
            df = df.loc[contained_points]
            
            df_all = pd.concat([df_all, df])
            if df.empty:
                print(f"No matching coordinates found in file: {file}")
            else:
                print(f"Matching coordinates found in file: {file}")
            bar()
    print("Files processed.")
    return df_all


def save_xyz(file: pd.DataFrame):
    save_filename = fd.asksaveasfilename(defaultextension='.xyz')
    if not save_filename:
        print("Filename empty... Abort.")
        return
    if not save_filename.endswith('.xyz'):
        save_filename = save_filename + '.xyz'
    file.to_csv(save_filename, sep=" ", header=None, index=False)

def _path_file_decider(file_contents: np.ndarray) -> str:
    path_type: str = ''
    number_columns = file_contents.shape[1]
    if number_columns == 4:
        path_type = 'p*xyz'
    elif number_columns == 2:
        path_type = 'xy'
    return path_type

def path_file_cropper(path_file: np.ndarray) -> np.ndarray:
    path_type = _path_file_decider(path_file)
    if path_type == 'p*xyz':
        path_file = path_file[:,[1,2]]
    elif path_type == 'xy':
        pass
    return path_file

def xyz_files_from_dialog() -> list:
    files = fd.askopenfilenames(title='Choose xyz-file(s)')
    xyz_files = [file for file in files if file.endswith('.xyz')]
    print("xyz-files loaded.")
    return xyz_files

def path_from_file() -> list:
    path_file = fd.askopenfilename(title='Choose path-file')
    path_list = np.genfromtxt(path_file, delimiter=' ')
    path_list = path_file_cropper(path_list)
    print("Path loaded.")
    return path_list 

