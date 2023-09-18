from flask.views import MethodView
from flask import render_template, request
import os
import re
import re
from services.picture_generator_service import picturegenerator


class ViewerView(MethodView):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app

    def get(self, filename):
        pos = request.args.get('pos', default=0, type=int)
        theme = request.args.get('theme', default='', type=str)
        if theme != '':
            self.app.config['THEME'] = theme
        else:
            theme = self.app.config['THEME']
        #print(theme)

        ## fetch the file
        filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename + ".txt")
        if not os.path.isfile(filepath):
            return "File not found", 404

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        ## fetch the content, which is then used as prompt for the stable diffusion API
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

        ## generate the picture
        picturegenerator(self.app.config['STABLE_DIFFUSION_URL'], f"A {theme} image of: " + content, os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}.png'))
        thumbnail = os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}.png')

        return render_template('viewer.html', filename=filename, content=content, thumbnail=thumbnail, nextpos=pos+1, prevpos=pos-1)
