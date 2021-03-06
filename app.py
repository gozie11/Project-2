import os
from os import abort
from urllib import request

import PyPDF2
from flask import Flask, render_template, request, url_for
from flask_bootstrap5 import Bootstrap
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
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
        return redirect(url_for("display", usr=user))
    return render_template('upload.html')


@app.route('/<usr>', methods=['GET', 'POST'])
def display(usr):
    pdfFileObj = open('data/sample_resume.pdf', 'rb')
    # Creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # Getting number of pages in pdf file
    pages = pdfReader.numPages
    # Loop for reading all the Pages
    for i in range(pages):
        # Creating a page object
        pageObj = pdfReader.getPage(i)
        # Printing Page Number
        print("Page No: ", i)
        # Extracting text from page
        # And splitting it into chunks of lines
        text = pageObj.extractText().split('\n')
        # Finally the lines are stored into list
        # For iterating over list a loop is used

        user['name'] = text[5:9]
        user['address'] = text[10:13]
        user['phonenum'] = text[14:17]
        user['email'] = text[18]
        user['info'] = text[19:]

        # print(user['name'])

        phonenum = ''.join(user['phonenum'])
        address = ''.join(user['address'])
        name = ''.join(user['name'])
        info = ''.join(user['info'])
        email = ''.join(user['email'])

        # make a list using all the elements in user['name]

        for i in range(len(text)):
            # Printing the line
            # Lines are separated using "\n"
            print(text[i], end="\n")
            # For Separating the Pages

    open('static/application_output.txt', "w").close()
    f = open('static/application_output.txt', 'w')
    f.write(name + '\n')
    f.write(address+ '\n')
    f.write(phonenum+ '\n')
    f.write(email+ '\n')
    f.write(info+ '\n')

    # closing the pdf file object
    pdfFileObj.close()

    if request.method == 'POST':
        return redirect(url_for("index", usr=user))

    return render_template('display.html',
                           usr=user,
                           name=name,
                           phonenum=phonenum,
                           address=address,
                           info=info)


if __name__ == '__main__':
    app.run()
