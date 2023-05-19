#!/usr/bin/env python3

import argparse
import pytesseract
import os

from pdf2image import convert_from_path
from tkinter import filedialog, ttk, END, Frame, Text

def on_keyword_found(progress, keyword_index, found_str):
    print(found_str)
    update_progress(progress)

def update_progress(progress):
    bar_length = 20
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1

    block = int(round(bar_length * progress))
    text = 'Progress: [{0}] {1:.1f}%'.format(
        '#' * block + '-' * (bar_length - block), progress * 100
    )
    print(text, end='\r')

def search(path, keyword_list, found_action):
    image_list = convert_from_path(path)
    keyword_nb = len(keyword_list)
    nb_step = len(image_list) * keyword_nb
    for page_number, page_data in enumerate(image_list):
        text = pytesseract.image_to_string(page_data)
        for keyword_index, keyword in enumerate(keyword_list):
            if keyword in text:
                found_action(
                    (page_number * keyword_nb + keyword_index) / nb_step,
                    keyword_index,
                    'Found %s page %s             ' % (keyword, page_number),
                )

class Application(ttk.Frame):
    def __init__(self, keyword_list, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets(keyword_list)
        self.keyword_found_label_list = []

    def create_widgets(self, keyword_list):
        self.select_file_button = ttk.Button(
            self,
            text='Select file',
            command=self.select_file,
        )
        self.select_file_button.grid()

        self.select_file_label = ttk.Label(self)
        self.select_file_label.grid(row=0, column=1)

        self.keyword_list_label = ttk.Label(self, text="Searched keywords")
        self.keyword_list_label.grid()

        self.keyword_list_text = Text(self, height=5)
        self.keyword_list_text.insert(END, '\n'.join(keyword_list))
        self.keyword_list_text.grid(row=1, column=1)

        self.search_keywords_button = ttk.Button(
            self,
            text='Search keywords',
            command=self.display_found_keywords,
        )
        self.search_keywords_button.grid()

        self.progressbar = ttk.Progressbar(
            self,
            length=self.keyword_list_text['width'] * 8
        )
        self.progressbar.grid(row=2, column=1)

        self.quit_button = ttk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=4)

    def display_found_keywords(self):
        self.progressbar.configure(value=0, maximum=1)
        self.progressbar.update()

        keyword_list = [keyword
            for keyword in self.keyword_list_text.get('1.0', END).split('\n')
            if keyword
        ]

        for label in self.keyword_found_label_list:
            label.destroy()
        self.keyword_found_label_list = []
        for index in range(len(keyword_list)):
            label = ttk.Label(self)
            label.grid(row=3, column=index) 
            self.keyword_found_label_list.append(label)

        search(self.filename, keyword_list, self.on_keyword_found)
        self.progressbar.configure(value=1)

    def on_keyword_found(self, progress, keyword_index, found_str):
        self.progressbar.configure(value=progress)
        self.progressbar.update()

        label = self.keyword_found_label_list[keyword_index]
        label.configure(text='%s%s\n' % (label['text'], found_str))
        label.update()

    def select_file(self):
        self.filename = filedialog.askopenfilename(
            title='Select file',
            filetypes=(('PDF', '*.pdf'),),
        )
        if self.filename:
            self.select_file_label.configure(
                text=os.path.basename(self.filename),
            )

parser = argparse.ArgumentParser()
parser.add_argument('--cli', action='store_true')
parser.add_argument('-f', '--file')
parser.add_argument(
    '-k',
    '--keyword_list',
    nargs='+',
    default=['vidéoprotection']
)
args = parser.parse_args()

if not args.cli:
    app = Application(args.keyword_list)
    app.master.title('NLVP')
    app.mainloop()
else:
    if args.file is None:
        parser.error('Requiring file path for cli mode')
    search(args.file, args.keyword_list, on_keyword_found)
    update_progress(1)
    print()
