#!/bin/py

'''
ChatGPT4 Prompt:
Write a python program which will convert an PDF input file into a plain-text string.
''' 
# --> leads to old API code, which is not working anymore

'''
BING-Chat Prompt:
python convert pdf to string
'''
# --> generates API code which is actual and working

# ==> nevertheless, OCR in PyPDF2 is not working well.

import PyPDF2

def pdf_to_text(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Replace 'path/to/your/file.pdf' with the actual path to your PDF file
pdf_text = pdf_to_text('tales/Machine_stops.pdf')

if pdf_text is not None:
    print(pdf_text)
