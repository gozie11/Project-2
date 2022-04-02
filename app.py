import os
from os import abort
from urllib import request

import PyPDF2
from flask import Flask, render_template, request
from flask_bootstrap5 import Bootstrap
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS']=['.pdf']
app.config['UPLOAD_PATH'] = 'data'
bootstrap = Bootstrap(app)

user = {}


@app.route('/')
def index():  # put application's code here
    return render_template("index.html", user=user)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return render_template('display.html')
    return render_template('upload.html')


if __name__ == '__main__':
    app.run()
