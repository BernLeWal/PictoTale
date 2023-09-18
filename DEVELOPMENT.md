# PictoTale
Development Steps

## Web-Application

### Pre-Requisites: Install FLask WebServer
```
pip install flask
```

1. Generate the initial web-project
```
ChatGPT4 prompt:
Create a web application project named PictoTale with all required files and directory structure. The backend should be written completely in python and the frontend webpages should be served by a pythion framework. The main web-page should contain a big image in the center, a text description below the picture, a "Next" and "Prev" button below the text and the title with a settings-button on the very top above the picture. Provide the HTML files and CSS and structure for static files.
```

2. Generate the ebook upload page
```
Add a file upload page which should contain an introduction text in the top center, a big area to drop the file to upload below the introduction, a "Upload" and a "Cancel" button below the drop-area and the title with a home-button on the very top above the instruction text.
The backend python code should take the file uploaded via the frontend and save it into a uploads directory.
```


## PDF-Conversion

### Tale/Novel Preparations
The application will generate an interacive picture-book of the text provided by tale/Novel text files. 

For the application to be able to read the content (only) and distinguish between chapters, paragraphs and sentences you need to do the following preparation steps:
1. Convert PDF, EPUB,... to a plain-text file. Take out all headers, footers, footnotes etc. which do not belong to the story
2. Generate a text-file structure as follows:

  * Every single sentence (in the original text may stop with ".") ends with CR/LF
  * Paragraphs are separated via NewLine
  * Chapters start with a sentence which starts itself with a number



* To Convert PDF-files to plain-text
```
pip install PyPDF2
pip install pdfminer
```

