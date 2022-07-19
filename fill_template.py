import argparse
import os
from pathlib import Path
import subprocess

from jinja2 import Template


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("short_name", type=str)
    parser.add_argument("--full_name", type=str)
    parser.add_argument("--package_name", type=str)
    parser.add_argument("--package_directory", type=str)
    args = parser.parse_args()

    if args.full_name is None:
        args.full_name = args.short_name

    if args.package_name is None:
        args.package_name = f"neptune_{args.short_name}"

    if args.package_directory is None:
        args.package_directory = f"neptune-{args.short_name}"

    return args


def should_skip(path):
    if str(path).startswith(".git"):
        return True
    if path.is_dir():
        return True
    if str(path) == str(Path(__file__).name):
        return True
    return False


def create_file_from_template(template_path, out_file_path, args):
    os.makedirs(new_path.parent, exist_ok=True)

    with open(template_path, "r") as file:
        template = file.read()

    with open(out_file_path, "w") as file:
        (
            Template(template)
            .stream(
                short_name=args.short_name,
                full_name=args.full_name,
                package_name=args.package_name,
                package_directory=args.package_directory,
            )
            .dump(file)
        )


if __name__ == "__main__":

    args = parse_args()

    BASE_PATH = Path(".")
    NEW_BASE_PATH = BASE_PATH.resolve().parent / args.package_directory

    if NEW_BASE_PATH.exists():
        raise RuntimeError(f"{NEW_BASE_PATH} path already exists")

    for template_path in BASE_PATH.rglob("*"):

        if should_skip(template_path):
            continue

        new_path = NEW_BASE_PATH / str(template_path).replace(
            "neptune_integration_template", args.package_name
        )

        print(f"Creating: {str(template_path):50s} -> {new_path}")

        create_file_from_template(template_path, new_path, args)

    print("\nFormatting the code:")

    run = subprocess.run(["black", NEW_BASE_PATH], capture_output=True)

    print(run.stdout.decode("utf-8"))
    print(run.stderr.decode("utf-8"))
