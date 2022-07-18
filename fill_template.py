import argparse
import os
from pathlib import Path

from jinja2 import Template


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("short_name", type=str)
    parser.add_argument("--full_name", type=str)
    parser.add_argument("--package_name", type=str)
    parser.add_argument("--package_directory", type=str)
    args = parser.parse_args()

    short_name = args.short_name

    if args.full_name is None:
        full_name = short_name
    else:
        full_name = args.full_name

    if args.package_name is None:
        package_name = f"neptune_{short_name}"
    else:
        package_name = args.package_name

    if args.package_directory is None:
        package_directory = f"neptune-{short_name}"
    else:
        package_directory = args.package_directory

    BASE_PATH = Path(".")
    NEW_PATH = BASE_PATH.resolve().parent / package_directory

    for path in BASE_PATH.glob("**/*"):

        if str(path).startswith(".git"):
            continue
        if path.is_dir():
            continue
        if str(path) == str(Path(__file__).name):
            continue

        new_path = NEW_PATH / str(path).replace(
            "neptune_integration_template", package_name
        )

        print("Creating:", new_path)
        os.makedirs(new_path.parent, exist_ok=True)

        with open(path, "r") as file:
            template = file.read()

        with open(new_path, "w") as file:
            (
                Template(template)
                .stream(
                    short_name=short_name,
                    full_name=full_name,
                    package_name=package_name,
                    package_directory=package_directory,
                )
                .dump(file)
            )
