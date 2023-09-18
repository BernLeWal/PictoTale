# PictoTale
Hear & See Your Novel

A case study to generate a full new application from srcatch with the help of generative-AI.

As a start also the application name was generated.
```
ChatGPT4 Prompt: 
Give me five suggestions for a title/name of the following app: The application will create a interactive picture book of a provided text novel, and will read it to the user.
```

## Pre-Requisites

Install the required packages
```
pip install -r requirements.txt
```


* To Convert PDF-files to plain-text
```
pip install PyPDF2
pip install pdfminer
```

## Tale/Novel Preparations
The application will generate an interacive picture-book of the text provided by tale/Novel text files. 

For the application to be able to read the content (only) and distinguish between chapters, paragraphs and sentences you need to do the following preparation steps:
1. Convert PDF, EPUB,... to a plain-text file. Take out all headers, footers, footnotes etc. which do not belong to the story
2. Generate a text-file structure as follows:

  * Every single sentence (in the original text may stop with ".") ends with CR/LF
  * Paragraphs are separated via NewLine
  * Chapters start with a sentence which starts itself with a number

