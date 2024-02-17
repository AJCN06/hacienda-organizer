from PIL import Image
from pytesseract import *
from .files_organizer import load_new_pictures

important_lines = [
    'Tipo de Transaccion',
    'Monto',
    'Comercio',
    'Autorizacion',
    'Referencia',
    'Fecha'
]


def read_images(file_path):
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    summarized = {}

    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    lines = text.splitlines()

    summarized["original_path"] = file_path
    for line in lines:
        for key in important_lines:
            if line.startswith(key):
                if key != 'Fecha':
                    summarized[key] = line.split(':')[-1]
                else:
                    summarized[key] = line.replace("Fecha: ", "")
    return summarized


def read_new_pictures():
    pictures = load_new_pictures()
    data = []
    for picture in pictures:
        text = read_images(picture)
        if 'Autorizacion' in text.keys():
            data.append(text)
    return data
