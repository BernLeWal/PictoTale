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
        posSentence = request.args.get('sentence', default=0, type=int)
        theme = request.args.get('theme', default='', type=str)
        if theme != '':
            session['THEME'] = theme
        else:
            if 'THEME' in session:
                theme = session['THEME']
        if theme == 'Default':
            theme = ''

        ## fetch the file
        filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename + ".txt")
        if not os.path.isfile(filepath):
            return "File not found", 404
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        ## fetch the content, which is then used as prompt for the stable diffusion API
        paragraphs = re.split(r'\n\s*\n', content)

        nextpos = pos
        nextSentence = posSentence

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
            print( f'Initial Paragraph: {content}\n')
            content = content.replace('\n',' ').replace('\r',' ').replace('“', '"').replace('”', '"') #.replace('’', "'").replace('‘', "'" )

            while not bool(re.search(r'\.\s*$', content)) and not bool(re.search(r'"\.\s*$', content)):
                nextpos += 1
                content += paragraphs[nextpos if nextpos < len(paragraphs) else 0]
            nextpos += 1 if nextpos < len(paragraphs) else 0

            content = content.replace('\n',' ').replace('\r',' ').replace('“', '"').replace('”', '"') #.replace('’', "'").replace('‘', "'" )
            print( f'Complete Paragraph: {content}\n' )

            sentences = extract_sentences(content)
            print( f'Sentences: {sentences}\n' )

            content = ""
            descriptions = ""
            speak = ""
            while not len(descriptions) > 100 and nextSentence < len(sentences):
                sentence, isSpeaking = sentences[nextSentence]
                if isSpeaking:
                    speak += f'{sentence} \n'                    
                    content += f'"{sentence}" \n'
                else:
                    descriptions += f'{sentence} \n'
                    content += f'{sentence} \n'
                nextSentence += 1
            print( f'Description: {descriptions}\n')
            print( f'Speech: {speak}\n')
            if nextSentence < len(sentences):
                nextpos = pos
            else:
                nextSentence = 0

            # generate the picture
            picturegenerator(self.app.config['STABLE_DIFFUSION_URL'], f"A ({theme}:{self.app.config['THEME_EMPHATIZE_RELATIVE']}) image of: " + descriptions, os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}-{posSentence}.png'))
            thumbnail = os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}-{posSentence}.png')

            # generate the speeches
            if speak != "":
                speechfile = os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}-{posSentence}.mp3')
                create_audio(speak, speechfile)


        return render_template('viewer.html', filename=filename, content=content, thumbnail=thumbnail, speechfile=speechfile, nextpos=nextpos, nextsentence=nextSentence, prevpos=pos-1, theme=theme)
