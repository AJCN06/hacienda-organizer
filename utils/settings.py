from os import makedirs
from os.path import join, exists

REGISTER_EMAIL = ""

NEW_INVOICES_PATH = join(".", "resources", "new", "invoices")
NEW_PICTURES_PATH = join(".", "resources", "new", "pictures")
PROCESSED_PATH = join(".", "resources", "processed")
SUMMARIES_PATH = join(".", "resources", "summaries")
TEMP_PATH = join(".", "resources", "temp")


def setup():
    for path in [NEW_INVOICES_PATH, NEW_PICTURES_PATH, PROCESSED_PATH, SUMMARIES_PATH]:
        if not exists(path):
            makedirs(path)


def handle_empty(key, data):
    return data[key] if key in data else None
