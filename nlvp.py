#!/usr/bin/env python3

import argparse
import pytesseract
from pdf2image import convert_from_path

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

keyword_list = ['vidéoprotection']

for page_number, page_data in enumerate(convert_from_path(args.filename)):
    text = pytesseract.image_to_string(page_data)
    for keyword in keyword_list:
        if keyword in text:
            print('Found %s page %s' % (keyword, page_number))
