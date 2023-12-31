from flask.views import MethodView
from flask import render_template, request, redirect, url_for
import os
import services.pdf_parser_service as pdf_parser_service
import services.pdf2image_service as pdf2image_service
from services.picture_generator_service import picturegenerator

class UploadView(MethodView):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app

    def get(self):
        return render_template('upload.html')

    def post(self):
        # handle file upload
        file = request.files['file']
        if file:
            filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # convert to plain-text
            text = pdf_parser_service.pdfparser(filepath)
            txtfilepath = filepath.replace('.pdf', '.txt')
            with open(txtfilepath, 'w', encoding='utf-8') as f:
                f.write(text)

            # generate thumbnail image for the file
            pngfilepath = filepath.replace('.pdf', '.png')
            # create an image from the first page
            #pdf2image_service.pdf2image(filepath, pngfilepath)
            # generate an image from the title (the first paragraph)
            picturegenerator(self.app.config['STABLE_DIFFUSION_URL'], text.split('\n')[0], pngfilepath)
            
            return redirect(url_for('gallery'))

        return "No file uploaded", 400
