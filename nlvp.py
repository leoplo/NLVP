from pdf2image import convert_from_path
import pytesseract

pdf_path = 'Recueil+N°254+sp+du+03+Novembre+2021.pdf'
keyword_list = ['vidéoprotection']

for page_number, page_data in enumerate(convert_from_path(pdf_path)):
    text = pytesseract.image_to_string(page_data)
    for keyword in keyword_list:
        if keyword in text:
            print('Found %s page %s' % (keyword, page_number))
