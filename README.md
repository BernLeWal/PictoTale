# PictoTale
Hear & See Your Novel

PictoTale is an ebook reader, which will go through an uploaded ebook paragraph wise. 
Per paragraph it will present a AI-generated picture of the descriptive tests of the paragraph 
and read out the texts of all conversations found there. 

It is a case study to generate a full new application from srcatch with the help of generative-AI.

## Pre-Requisites

Install the required packages
```
pip install -r requirements.txt
```
See the contents of [requirements.txt](requirements.txt) to check out which libraries are needed


You need to have an installation of stable diffusion available, per default on your local machine (http://localhost:7860), with --api enabled.

## Run the application
```
python app.py
```

Open the web-page in the browser, start with http://localhost:5000/upload
