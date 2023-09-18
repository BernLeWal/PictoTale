#!/bin/py
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pdfparser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # convert to plain-text
            text = pdfparser.pdfparser(filepath)
            filepath = filepath.replace('.pdf', '.txt')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)

            return redirect(url_for('index'))
    return render_template('upload.html')
    
@app.route('/gallery')
def gallery():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.txt')]
    file_details = [
        {
            "filename": f,
            "thumbnail": (os.path.join(app.config['UPLOAD_FOLDER'], f.replace('.txt', '.jpg'))) if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], f.replace('.txt', '.jpg'))) else '/static/images/ebook.png'
        }
        for f in files
    ]
    return render_template('gallery.html', file_details=file_details)

@app.route('/viewer/<filename>')
def viewer(filename):
    return render_template('viewer.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
