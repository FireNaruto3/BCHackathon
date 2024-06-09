from flask import Flask, render_template, request, redirect, url_for
import os


app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/eyeDisease.html")
def test():
    return render_template("eyeDisease.html")

@app.route("/upload", methods = ["POST"])
def upload():
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return f'File uploaded successfully. Saved at: {file_path}'


@app.route("/question", methods = ["POST"])
def question():
    return redirect(url_for('home'))

if(__name__ == '__main__'):
    app.run(debug = True)