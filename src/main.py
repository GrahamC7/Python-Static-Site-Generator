import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
        if not base_path.startswith("/"):
            base_path = "/" + base_path
        if not base_path.endswith("/"):
            base_path += "/"

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages from content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

    print("Done.")


main()
