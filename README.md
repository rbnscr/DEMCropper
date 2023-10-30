# DEMCropper 🐱‍👓

## Description

**D**igital **E**levation **M**odels often are  downloadable as .xyz-files from open repositories. In Germany, DEMs are provided by the government to the general public in a 1 by 1m raster (see [here](https://www.opengeodata.nrw.de/produkte/geobasis/hm/dgm1_xyz/dgm1_xyz/)). Provided are single tiles, which each contain 10^6 x/y/z-coordinates. Extracting useful shapes out of these tiles, can be tedious and time-consuming. 

Hence, **DEMCropper** is able to "cut" a slice out of one or multiple DEM-files using a user-defined path (x/y or p*/x/y/z) (see examples). The program contains a GUI to check your path / shape and a CLI for ease of use.

## How to run

1. Install [Python 3.10](https://www.python.org/downloads/) or higher.
2. Clone the repo using git, or download via the link.

``` git
git clone https://github.com/rbnscr/DEMCropper
```

3. Navigate the command window to the unpacked project folder, and setup a virtual python environment. Also, install the requirements.

``` bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r .\requirements.txt 
```

4. Run the GUI or the CLI interface. The virtual enviroment has to be active, as indicated by (.venv).

``` bash
.venv\Scripts\activate
python DEMCropper.py            # For GUI
python DEMCropper.py -c         # For CLI
```

5. In Powershell you might need to enable the execution of script-files:
``` powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.venv\Scripts\activate.ps1
```

## Example
![xyzMerge](title.png)