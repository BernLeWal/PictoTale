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

## Stable-Diffusion Agent

Python program for integrating Stable Diffusion, which runs as a separate application instance.

```
pip install requests
pip install pillow
```

