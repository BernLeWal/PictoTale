from flask.views import MethodView
from flask import render_template
import os

class GalleryView(MethodView):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app

    def get(self):
        files = [f for f in os.listdir(self.app.config['UPLOAD_FOLDER']) if f.endswith('.txt')]
        file_details = [
            {
                "filename": f,
                "thumbnail": (os.path.join(self.app.config['UPLOAD_FOLDER'], f.replace('.txt', '.jpg'))) if os.path.exists(os.path.join(self.app.config['UPLOAD_FOLDER'], f.replace('.txt', '.jpg'))) else '/static/images/ebook.png'
            }
            for f in files
        ]
        return render_template('gallery.html', file_details=file_details)
