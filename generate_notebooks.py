import argparse
import os
import subprocess
import sys
from pathlib import Path

PAGES_PATH = "pages/notebooks"

def main():
    args = _parse_args()
    folder_path = args.folder
    # output_path = args.output
    file_paths = [f for f in os.listdir(folder_path) if folder_path.joinpath(f).suffix == ".ipynb"]
    nav_order = 1
    for notebook in file_paths:
        notebook_path = folder_path / notebook
        _call(
                ["jupyter", "nbconvert", notebook_path, "--to", "html"],
                "Building manual...",
                f"Could not build manual.",
            )
        readable_notebook = str(notebook).split(".ipynb")[0].replace("_", " ").title()
        notebook_link = str(notebook).split(".ipynb")[0].replace("_", "")
        html_path = str(notebook_path).replace("ipynb", "html").replace("\\", "/").replace("_includes/", "")
        MARKDOWN_FILE = [
            "---\n",
            "layout: default\n",
            f"title: {readable_notebook}\n",
            "parent: Code Examples\n",
            f"permalink: /notebooks/{notebook_link}/\n",
            f"nav_order: {nav_order}\n",
            "---\n",
            f"{{% include notebook.html path=\"{html_path}\" %}}",
            ]
        nav_order += 1
        with open(f"{PAGES_PATH}/{str(notebook).removesuffix('ipynb')}md", "w") as file:
            file.writelines(MARKDOWN_FILE)

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        help="PDF output file",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "-f",
        "--folder",
        help="PDF output folder",
        type=Path,
        default=None,
        required=True,
    )
    args = parser.parse_args()
    return args


def _call(args: list[str], pre: str = None, err: str = None, exit_on_err=True):
    """Run a command in a subprocess.

    Args:
        args (list[str]): command to run as list of parts
        pre (str): optional text to print before command
        err (str): optional error message to display if subprocess fails
        exit_on_err (bool): whether to exit with code 1 if subprocess fails
    """
    args = [str(x) for x in args]

    if pre:
        print(pre)
    print("Running command:", " ".join(args))
    try:
        subprocess.check_call(args)
    except Exception as e:
        print(f"Subprocess failed: {e}")
        if err:
            print(err)
        if exit_on_err:
            sys.exit(1)


if __name__ == "__main__":
    main()
