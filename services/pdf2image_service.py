#!/bin/py
import fitz  # PyMuPDF
import sys

def pdf2image(pdf_path, output_path):
    try:
        # Open the PDF file
        pdf = fitz.open(pdf_path)
        
        # Get the first page
        page = pdf[0]

        # Get the page as a pixmap (an image)
        pixmap = page.get_pixmap()

        # Save the image to the output path
        pixmap.save(output_path)

        print(f"Successfully saved the first page of {pdf_path} as {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Use the script from the command line: python script.py input.pdf output.png
if __name__ == "__main__":
    pdf_path = "experiments/Machine_stops.pdf"  #sys.argv[1]
    output_path = "Machine_stops.png"  #sys.argv[2]
    
    pdf2image(pdf_path, output_path)
