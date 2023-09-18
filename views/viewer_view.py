from flask.views import MethodView
from flask import render_template, request
import requests
import os
import re
import re
import io
import base64
from PIL import Image, PngImagePlugin


class ViewerView(MethodView):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app

    def get(self, filename):
        pos = request.args.get('pos', default=0, type=int)

        ## fetch the file
        filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
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
        payload = {
            "prompt": "A steampunk image of: " + content,
            "steps": 5
        }
        url = self.app.config['STABLE_DIFFUSION_URL']
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        r = response.json()
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save(os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}.png'), pnginfo=pnginfo)

        thumbnail = os.path.join(self.app.config['CACHE_FOLDER'], f'{filename}-{pos}.png')

        return render_template('viewer.html', filename=filename, content=content, thumbnail=thumbnail, nextpos=pos+1, prevpos=pos-1)
