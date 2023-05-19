#!/usr/bin/env python3

import argparse
import pytesseract
from pdf2image import convert_from_path

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-k', '--keyword_list', nargs='+', default=['vidéoprotection'])
args = parser.parse_args()

for page_number, page_data in enumerate(convert_from_path(args.filename)):
    text = pytesseract.image_to_string(page_data)
    for keyword in args.keyword_list:
        if keyword in text:
            print('Found %s page %s' % (keyword, page_number))
