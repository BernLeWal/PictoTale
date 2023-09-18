#!/bin/py
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from dotenv import load_dotenv
from views.home_view import HomeView
from views.upload_view import UploadView
from views.gallery_view import GalleryView
from views.viewer_view import ViewerView



# Logic to set up the application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['CACHE_FOLDER'] = os.environ.get('CACHE_FOLDER', 'cache')
app.config['STABLE_DIFFUSION_URL'] = os.environ.get('STABLE_DIFFUSION_URL', 'http://localhost:7860')


# Rules to connect the views
app.add_url_rule('/', view_func=HomeView.as_view('home'))
app.add_url_rule('/upload', view_func=UploadView.as_view('upload', app))
app.add_url_rule('/gallery', view_func=GalleryView.as_view('gallery', app))
app.add_url_rule('/viewer/<filename>', view_func=ViewerView.as_view('viewer', app))


# Static files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/cache/<filename>')
def cache_file(filename):
    return send_from_directory(app.config['CACHE_FOLDER'], filename)



# Application entry point
if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('cache'):
        os.makedirs('cache')
    app.run(debug=True)
