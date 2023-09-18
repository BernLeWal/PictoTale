#!/bin/py
import os
from flask import Flask, render_template, request, redirect, url_for
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

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
