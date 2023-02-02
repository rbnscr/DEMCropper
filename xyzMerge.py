import os
import pandas as pd
from alive_progress import alive_bar


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


def save_xyz(file: pd.DataFrame):
    print("Enter filename...")
    filename = input()
    file.to_csv(f"{filename}.xyz", sep=" ", header=None, index=False)
    print(f"File saved: {os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)}.xyz")

def end_loop():
    print("Re-run? (Y)")
    decider = input().capitalize()
    if decider == "Y" or decider =="":
        Main()

def Main():
    inputs = handle_inputs()
    # inputs = {"x0": 377500, "x1": 377999, "y0": 570000, "y1": 5703001}
    xyz_files = get_xyz_files()
    df_to_save = process_files(inputs, xyz_files)
    save_xyz(df_to_save)
    end_loop()

if __name__ == "__main__":
    Main()
