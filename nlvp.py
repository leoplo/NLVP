#!/usr/bin/env python3

import argparse
import pytesseract
import os

from pdf2image import convert_from_path
from tkinter import filedialog, ttk, END, Frame, Text

PROGRESS_BAR_STRING_SIZE = 38

def on_keyword_found(_, found_str):
    print(found_str)

def update_progress_bar(progress):
    bar_length = 20

    block = int(round(bar_length * progress))
    text = 'Progress: [{0}] {1:.1f}%'.format(
        '#' * block + '-' * (bar_length - block), progress * 100
    )
    print(text, end='\r')

def search(path, keyword_list, update_progress, found_action):
    update_progress(0)
    image_list = convert_from_path(path)
    for page_number, page_data in enumerate(image_list):
        text = pytesseract.image_to_string(page_data)
        for keyword_index, keyword in enumerate(keyword_list):
            if keyword in text:
                found_str = 'Found %s page %s' % (keyword, page_number)
                if len(found_str) < PROGRESS_BAR_STRING_SIZE:
                    found_str = '%s%s' % (found_str, ' ' * (PROGRESS_BAR_STRING_SIZE - len(found_str)))
                found_action(keyword_index, found_str)
        update_progress((page_number + 1) / len(image_list))

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
            length=self.keyword_list_text['width'] * 8,
            maximum=1,
        )
        self.progressbar.grid(row=2, column=1)

        self.quit_button = ttk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=4)

    def display_found_keywords(self):
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

        search(
            self.filename,
            keyword_list,
            self.update_progress,
            self.on_keyword_found,
        )

    def on_keyword_found(self, keyword_index, found_str):
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

    def update_progress(self, progress):
        self.progressbar.configure(value=progress)
        self.progressbar.update()

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
    search(args.file, args.keyword_list, update_progress_bar, on_keyword_found)
    print()
