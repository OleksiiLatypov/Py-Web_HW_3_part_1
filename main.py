import argparse
import shutil
from pathlib import Path
from shutil import move, unpack_archive
from threading import Thread
import logging
import re

"""
py main.py --source 'path to folder'
"""

parser = argparse.ArgumentParser(description='App for sorting folder')
parser.add_argument('-s', '--source', help="Source folder", required=True)  # option that takes a value
# parser.add_argument('-o', '--output', default='dist')
args = vars(parser.parse_args())  # object -> dict
source = args.get('source')
# output = source  # args.get('output')

folders = []
images = (".jpeg", ".png", ".jpg", ".svg")
video = (".avi", ".mp4", ".mov", ".mkv")
documents = (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx", ".csv", ".html", ".rtf")
archive = ('.zip', ".gz", ".tar")


def grabs_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def sort_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            if ext in images:
                new_path = output_folder / 'IMAGES'
                try:
                    new_path.mkdir(exist_ok=True, parents=True)
                    move(el, new_path / el.name)
                except OSError as e:
                    logging.error(e)
            elif ext in documents:
                new_path = output_folder / 'DOCUMENTS'
                try:
                    new_path.mkdir(exist_ok=True, parents=True)
                    move(el, new_path / el.name)
                except OSError as e:
                    logging.error(e)
            elif ext in video:
                new_path = output_folder / 'VIDEO'
                try:
                    new_path.mkdir(exist_ok=True, parents=True)
                    move(el, new_path / el.name)
                except OSError as e:
                    logging.error(e)
            elif ext in archive:
                new_path = output_folder / 'ARCHIVES'
                try:
                    new_path.mkdir(exist_ok=True, parents=True)
                    shutil.unpack_archive(el, new_path / el.name)
                except OSError as e:
                    logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = base_folder  # Path(output)

    folders.append(base_folder)
    grabs_folder(base_folder)
    threads = []
    for folder in folders:
        th = Thread(target=sort_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    logging.info('Folder has been sorted')
