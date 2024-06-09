from flask import Flask, render_template, request, session
import os
from classify import classify


app = Flask(__name__)
app.secret_key = "69420"

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

    predicted_class_name, confidence_item = classify(file_path)

    session["disease"] = predicted_class_name
    session["percentage"] = confidence_item * 100
    
    return render_template("results.html")
    # return f'There is a {confidence_item * 100}% chance that you have {predicted_class_name}'
    # return classify(file_path)
    # return f'File uploaded successfully. Saved at: {file_path}'

@app.route("/results")
def results():
    disease = session.get("disease")
    percentage = session.get("percentage")

    return render_template("results.html", disease = disease, percentage = percentage)

if(__name__ == '__main__'):
    app.run(debug = True)