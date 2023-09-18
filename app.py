#!/bin/py
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pdfparser
import re

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
    pos = request.args.get('pos', default=0, type=int)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(filepath):
        return "File not found", 404

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    paragraphs = re.split(r'\n\s*\n', content)
    if pos == 0:
        for i, paragraph in enumerate(paragraphs):
            if re.match(r'^\d.*$', paragraph.split('\n')[0]):
                pos = i+1 if i+1 < len(paragraphs) else i
                content = paragraphs[pos]
                break
    else:
        content = paragraphs[pos if pos < len(paragraphs) else 0]

    while not content.endswith('.'):
        pos += 1
        content += paragraphs[pos if pos < len(paragraphs) else 0]

    thumbnail = (os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.txt', '.jpg'))) if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.txt', '.jpg'))) else '/static/images/ebook.png'

    return render_template('viewer.html', filename=filename, content=content, thumbnail=thumbnail, nextpos=pos+1, prevpos=pos-1)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
