import argparse
from src import app, cli

def handle_args():
    parser = argparse.ArgumentParser(prog="DEMCropper",
                                     description="Crop xyz-files using a 2D path")
    parser.add_argument(
        "--cli",
        dest="cli_flag",
        type=bool,
        required=False,
        default=False,
        help="Set to true to use the CLI instead of GUI (default: False)"
    )
    return parser.parse_args()

def Main():
    args = handle_args()

    if args.cli_flag == True:
        cli.Main()
    elif args.cli_flag == False:
        app.Main()

if __name__ == "__main__":
    Main()