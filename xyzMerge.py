import os
import pandas as pd
from alive_progress import alive_bar
import numpy as np

import tkinter as tk
import tkinter.filedialog as fd

from matplotlib.path import Path

def handle_inputs():
    coordinates_keys = ["x0", "x1", "y0", "y1"]
    coordinates = dict.fromkeys(coordinates_keys)
    for key in coordinates.keys():
        validity_check = False
        while validity_check is False:
            print(f"Select {key}:")
            coordinate_input = input()
            try:
                coordinate_input = int(coordinate_input)
                coordinates[key] = coordinate_input
                validity_check = True
            except ValueError:
                print("Input has to be a number.")
                validity_check = False
    if coordinates["x0"] > coordinates["x1"]:
        x0_ = coordinates["x1"]
        coordinates["x1"] = coordinates["x0"]
        coordinates["x0"] = x0_

    if coordinates["y0"] > coordinates["y1"]:
        y0_ = coordinates["y1"]
        coordinates["y1"] = coordinates["y0"]
        coordinates["y0"] = y0_

    return coordinates


def get_xyz_files():
    xyz_files = []
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith(".xyz")]:
            if dirpath != ".":
                xyz_files.append(os.path.join(dirpath, filename))
    print("Files found:")
    print(*xyz_files, sep="\n")
    print("Continue? (Y/n)")
    decider = input().capitalize()
    print(decider)
    if decider == "Y" or decider == "":
        return xyz_files
    else:
        exit()


def process_files(target_coordiantes, xyz_files):
    df_all = pd.DataFrame(columns=["x", "y", "z"])
    with alive_bar(len(xyz_files),dual_line=True) as bar:
        for file in xyz_files:
            bar.text = f"-> Processing file: {file}, please wait..."
            df = pd.read_table(
                file, delim_whitespace=True, header=None, names=["x", "y", "z"]
            )
            df = df.loc[
                (df["x"] >= target_coordiantes["x0"])
                & (df["x"] <= target_coordiantes["x1"])
                & (df["y"] >= target_coordiantes["y0"])
                & (df["y"] <= target_coordiantes["y1"])
            ]
            df_all = pd.concat([df_all, df])
            if df.empty:
                print(f"No matching coordinates found in file: {file}")
            else:
                print(f"Matching coordinates found in file: {file}")
            bar()
    return df_all

def process_files_poly(target_coordiantes, xyz_files):
    # p = Path([(target_coordiantes["x0"],target_coordiantes["y0"]),(target_coordiantes["x0"],target_coordiantes["y1"]),(target_coordiantes["x1"],target_coordiantes["y1"]),(target_coordiantes["x1"],target_coordiantes["y0"])])
    p = Path(target_coordiantes)
    print(p)
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
    return df_all


def save_xyz(file: pd.DataFrame):
    # print("Enter filename...")
    # filename = input()
    save_filename = fd.asksaveasfilename(defaultextension='.xyz')
    if not save_filename:
        print("Filename empty... Abort.")
        return
    if not save_filename.endswith('.xyz'):
        save_filename = save_filename + '.xyz'
    file.to_csv(save_filename, sep=" ", header=None, index=False)
    # file.to_csv(f"{filename}.xyz", sep=" ", header=None, index=False)
    # print(f"File saved: {os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)}.xyz")

def end_loop():
    print("Re-run? (Y)")
    decider = input().capitalize()
    if decider == "Y":
        Main()

def xyz_files_from_dialog() -> list:
    files = fd.askopenfilenames(title='Choose xyz-file(s)')
    xyz_files = [file for file in files if file.endswith('.xyz')]
    return xyz_files

def path_from_file() -> list:
    path_file = fd.askopenfilename(title='Choose path-file')
    path_list = np.genfromtxt(path_file, delimiter=' ')
    return path_list 

def Main():
    # root = tk.Tk()
    # root.title('test')
    # path_btn = tk.Button(root, text="Open path file", command=path_from_file).pack()
    # root.mainloop()

    path = path_from_file()

    # # inputs = handle_inputs()
    # # inputs = {"x0": 377500, "x1": 377999, "y0": 570000, "y1": 5703001}
    # inputs = {"x0": 0, "x1": 3.5, "y0": 1.5, "y1": 3.5}
    # # xyz_files = get_xyz_files()

    xyz_files = xyz_files_from_dialog()
    df_to_save = process_files_poly(path, xyz_files)
    if not df_to_save.empty:
        save_xyz(df_to_save)
    # end_loop()
    



if __name__ == "__main__":
    Main()


