from os import makedirs
from os.path import join, exists
import shutil
import glob
import re

from datetime import datetime
from .settings import PROCESSED_PATH, NEW_PICTURES_PATH, NEW_INVOICES_PATH


def clean_path(path):
    if not exists(path):
        makedirs(path)


def format_date(date):
    return datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')


def possible_date(data):
    match = re.search(r'(\d{8})', data)
    print(match, data)
    if match:
        return format_date(match.group(1))
    return None


def load_new_invoices():
    return load_files(join(NEW_INVOICES_PATH, "*.zip"))


def load_new_pictures():
    return load_files(join(NEW_PICTURES_PATH, "*.jpg"))


def load_files(target):
    return glob.glob(target)


def move_invoices(invoices: list):
    for invoice in invoices:
        move_invoice(invoice["original_path"], invoice["zip_name"])


def move_invoice(invoice, name=None):
    move_file(invoice, join(PROCESSED_PATH, "invoices"), name)


def move_pictures(pictures: list):
    for pic in pictures:
        move_picture(pic["original_path"])


def move_picture(picture: str, name=None):
    move_file(picture, join(PROCESSED_PATH, "pictures"), name)


def move_file(origin, destination, name=None):
    clean_path(destination)
    if name:
        destination = join(destination, name)
    shutil.move(origin, destination)
