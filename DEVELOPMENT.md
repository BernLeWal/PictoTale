# PictoTale
Development Steps

As a start also the application name was generated.
```
ChatGPT4 Prompt: 
Give me five suggestions for a title/name of the following app: The application will create a interactive picture book of a provided text novel, and will read it to the user.
```

## Web-Application

### Pre-Requisites: Install FLask WebServer
```
pip install flask
```

### Rapid generation of the prototype
Here follows the ChatGPT4 prompts:


1. Generate the initial web-project
```
Create a web application project named PictoTale with all required files and directory structure. The backend should be written completely in python and the frontend webpages should be served by a pythion framework. The main web-page should contain a big image in the center, a text description below the picture, a "Next" and "Prev" button below the text and the title with a settings-button on the very top above the picture. Provide the HTML files and CSS and structure for static files.
```

2. Generate the ebook upload page
```
Add a file upload page which should contain an introduction text in the top center, a big area to drop the file to upload below the introduction, a "Upload" and a "Cancel" button below the drop-area and the title with a home-button on the very top above the instruction text.
The backend python code should take the file uploaded via the frontend and save it into a uploads directory.
```

3. Generate the gallery page
```
Add a gallery page which should contain an 3x3 item view in the top center build out of all *.txt files which are in the uploads directory. if there is a corresponding *.jpg file existing for an item, then use this image as thumbnail, otherwise use a generic ebook symbol. Below each item there should be the name of the file displayed. When an item is clicked, then the frontend should redirect to the "viewer.html" template passing the filename as parameter. Below the items view there is a "Home" button. Provide the HTML files and CSS and modifications to the app.py.
```

3b. You need to add a route to access the uploaded files from the web-frontend
```
Modify app.py to add a route to read-only access the files of the uploads directory directly.
```

4. Generate the viewer page
```
Add to the viewer page a second parameter named "pos" which is optional and defaults to 0.
The backend of the viewer page should open the text file defined in the "filename" parameter and store it into a string variable.
When pos=0 then all characters of the string variable are skipped, until a number is showing up on the beginning of a line or sentence. The line containing that number should also be skipped.
Then keep all characters until a new paragraph - indicated with an empty line gap - shows up. The rest of the lines are skipped, too.
The resulting text should be shown in the viewer page in a description section below the picture.
```

5. Integrate Stable Diffusion
However, generative AI was of no help here:
- ChatGPT just provided generic HTTP request generation - without considering the stable diffusion API at all
- BingChat wrongly redirects to the stable diffusion clone/install instructions - did not correctly understand the question

At the end the stable diffusion webui just provides a direct link to the API with the sample-code used here.

6. Use configuration from environment variables
```
Change the app.py file in the way that the application configuration is provided in environmental variables or .env file instead of being hardcoded.
```

### Refactorings

1. Move view-backend in separate classes into the views module
```
Please refactor app.py so that the implementations of the endpoints will be moved to separate classes in the views subdirectory.
```

ATTENTION: the generated code / refactoring hints won't compile, because app is not passed to the view classes!

2. Get app variable into the view classes
```
Correct the upload_view.py program to get the app object.
```

--> Unfortunately ChatGPT4 was completely lost, and did not get the question right.

==> Solution was to manually fix this issue by generating ctor with the corresponding parameter :-)

### Add further proto features

1. Switch picture generation between different themes
```
Please remember the settings button in the index.html file. Modify the sources so that a popup-window with shows up when the settings button is clicked. The following menu items should be presented: Default, Steampunk, Cyberpunk, Photorealistic, Film Noir.
```

2. Store the selected theme in the session
```
Tell me how to store values in the session.
```

3. Create an image of the first page in the pdf-file
```
Please create python code using the PDFMiner library, which will read the first page of the input pdf file and store it as a image to be later used as a thumbnail in the gallery page.
```
--> Created a solution using the pdf2image library, which requires poppler installed on the OS, so we need to find a different library

```
please use a different framework than pdf2image to extract the first page as an image.
```

4. Extract the description (for picture generation) and speeches (for TTS) from the content
```
Write a python script which will from a given string extract all sentences within double-quotes to a variable called speeches and the rest to a variable called descriptions.
```

5. Introduce a TTS-engine to the application
```
Write a python code which will use a text-to-speech engine to create an audio from a string and will play this in the viewer.html.
```

```
Please adapt the html file to hide the audio control when no mp3 file is given.
```

```
Tell me how to autoplay the audiosource in the html file.
```

6. Try to optimize the output of the TTS
```
I want to add some pauses in the audio result of the gtts engine. Which characters do I have to add to the input string to do so?
```
--> The suggestions did not work, unfortunately ChatGPT does not know the gTTS good enough ;-)

Tried it with BING-Chat instead:
--> Returned even more suggestions (also mentioned the SSML input format), but all these still don't work

==> Reading the gTTS reference documentation will be required here!

7. Picture generation optimization: emphatise the theme
asked BING-Chat:
```
Tell me how I can use the promt to stable diffusion to enforce specific words.
```

### Trial 1: Apply a nice CSS-template: BuzzApp
used (https://www.free-css.com)[https://www.free-css.com] with search parameters: HTML5, responsive, 1 Column

Result was BuzzApp: https://www.free-css.com/free-css-templates/page161/buzzapp

1. Apply CSS-template to the application
```
Please help me with applying a predefined CSS-template to the application.
I have the following CSS file which uses bootstrap:
<pasted the styles.css file>

And a HTML file showing how the assents of this template is used:
<pasted the index.html file>
```
--> Suggestions from ChatGPT4 are very generic, just a checklist.
Nothing what support me for coding.
--> everything has to be done by hand (as before). ChatGPT4 was no help at all!

2. Manually applied BuzzApp in the index-page

ATTENTION: No help from ChatGPT!
--> It turned out, that this minimalistic CSS-template does not fit to well to the application and I would have to change the CSS files by myself to get an intermediate result. That's not what I wanted.


### Trial 2: Improve the CSS-template

```
OK, your last suggestion did not help me much, so please lets go one step back.
Please provide me with a enhanced CSS file to support a responsive design and a modern look and feel.
```

--> Design is ok (but not ambitious)

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
pip install pdfminer.six
```

* To Convert the first page of the PDF-file to an image
```
pip install pymupdf
```

## Stable-Diffusion Agent

Python program for integrating Stable Diffusion, which runs as a separate application instance.

```
pip install requests
pip install pillow
```

