from flask.views import MethodView
from flask import render_template, request, session
import os
import re
from services.picture_generator_service import picturegenerator
from services.sentences_extractor_service import extract_sentences
from services.tts_service import create_audio


class ViewerView(MethodView):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app

    def get(self, filename):
        ## retrieve the request/session parameters
        pos = request.args.get('pos', default=0, type=int)
        theme = request.args.get('theme', default='', type=str)
        if theme != '':
            session['THEME'] = theme
        else:
            if 'THEME' in session:
                theme = session['THEME']

        ## fetch the file
        filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename + ".txt")
        if not os.path.isfile(filepath):
            return "File not found", 404
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        ## fetch the content, which is then used as prompt for the stable diffusion API
        paragraphs = re.split(r'\n\s*\n', content)

        nextpos = pos
        content = ""
        speechfile = ""
        if pos == 0:
            # Show the title page
            for i, paragraph in enumerate(paragraphs):
                if re.match(r'^\d.*$', paragraph.split('\n')[0]):
                    nextpos = i+1 if i+1 < len(paragraphs) else i
                    break

            for i in range(nextpos-1):
                content += paragraphs[i] + '\n'

            thumbnail = os.path.join(self.app.config['UPLOAD_FOLDER'], f'{filename}.png')

        else:
            # Show the book pages and generate the pictures
            content = paragraphs[pos if pos < len(paragraphs) else 0]

            while not content.endswith('.'):
                nextpos += 1
                content += paragraphs[nextpos if nextpos < len(paragraphs) else 0]
            nextpos += 1 if nextpos < len(paragraphs) else 0

            content = content.replace('\n',' ').replace('\r',' ').replace('“', '"').replace('”', '"') #.replace('’', "'").replace('‘', "'" )
            print( f'Content: {content}\n' )
            sentences, descriptions = extract_sentences(content)

            # generate the picture
            print( f'Description: {descriptions}\n' )
            picturegenerator(self.app.config['STABLE_DIFFUSION_URL'], f"A {theme} image of: " + descriptions, os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}.png'))
            thumbnail = os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}.png')

            # generate the speeches
            speak = ""
            for i, sentence in enumerate(sentences):
                speak += f'{sentence} \n'
            print( f'Speech: {speak}\n')

            if speak != "":
                speechfile = os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}.mp3')
                create_audio(speak, speechfile)


        return render_template('viewer.html', filename=filename, content=content, thumbnail=thumbnail, speechfile=speechfile, nextpos=nextpos, prevpos=pos-1, theme=theme)
