import tkinter as tk
from tkinter import ttk

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.path import Path
import matplotlib.patches as patches

from .lib import *



root = tk.Tk()
root.title("DEG Merger")
root.geometry('1200x800')

# grid
root.columnconfigure((0), weight = 2)
root.rowconfigure((0,1,2,3), weight = 0)

# Functions
def load_path():
    global app_path_file_contents
    app_path_file_contents = path_from_file()
    plot_path()

def load_xyz_files():
    global app_xyz_files
    app_xyz_files = xyz_files_from_dialog()

def btn_process_files():
    global app_df_to_save
    app_df_to_save = process_files_poly(app_path_file_contents, app_xyz_files)
    plot_xyz_file()

def btn_save_xyz():
    save_xyz(app_df_to_save)

# Buttons
btn_load_path = ttk.Button(root, width="20", text = 'Load Path File',  command = lambda: load_path())
# btn_load_path.grid(row = 0, column = 0, sticky="nws")


btn_load_xyz = ttk.Button(root, width="20", text = 'Load xyz-File', command = lambda: load_xyz_files())
# btn_load_xyz.grid(row = 1, column = 0, sticky="nws")



btn_process_polygon = ttk.Button(root, width="20", text = 'Start Computation', command = lambda: btn_process_files())
# btn_process_polygon.grid(row = 2, column = 0, sticky="nws")


btn_save_xyz = ttk.Button(root, width="20", text = 'Save xyz-File', command = lambda: btn_save_xyz())
# btn_save_xyz.grid(row = 3, column = 0, sticky="nws")

btn_plot_path = ttk.Button(root, width="20", text = 'Plot path', command = lambda: plot_path())
# btn_plot_path.grid(row = 4, column = 0, sticky="nws")


def plot_xyz_file():
    x = app_df_to_save["x"]
    y = app_df_to_save["y"]
    ax_scatter = fig.add_subplot()
    ax_scatter.scatter(x, y)
    ax_scatter.set_xticklabels([])
    ax_scatter.set_yticklabels([])
    ax_scatter.set_xticks([])
    ax_scatter.set_yticks([])
    ax_scatter.set_xlim(plot_x_min, plot_x_max)
    ax_scatter.set_ylim(plot_y_min, plot_y_max)  

    canvas.draw()


def plot_path():
    global plot_x_min, plot_x_max, plot_y_min, plot_y_max
    path_to_plot = Path(app_path_file_contents)
    plot_x_min = min(app_path_file_contents[:,0])
    plot_x_max = max(app_path_file_contents[:,0])
    plot_y_min = min(app_path_file_contents[:,1])
    plot_y_max = max(app_path_file_contents[:,1])

    # Figure
    # fig = Figure(figsize=(8, 8), dpi=100)

    patch = patches.PathPatch(path_to_plot, facecolor='grey', lw=0)
    ax = fig.add_subplot()
    # ax.set_xlabel("x")
    # ax.set_ylabel("y")
    ax.set_xlim(plot_x_min, plot_x_max)
    ax.set_ylim(plot_y_min, plot_y_max)  

    ax.add_patch(patch)
    canvas.draw()

fig = Figure(figsize=(8, 8), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().pack(side=tk.RIGHT, anchor=tk.NE)
canvas.draw()
    


# Pack
btn_load_path.pack(side=tk.TOP, anchor=tk.NW)
btn_load_xyz.pack(side=tk.TOP, anchor=tk.NW)
btn_process_polygon.pack(side=tk.TOP, anchor=tk.NW)
btn_save_xyz.pack(side=tk.TOP, anchor=tk.NW)


# Run
root.mainloop()