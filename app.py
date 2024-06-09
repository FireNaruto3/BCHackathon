from flask import Flask, render_template, request, session, url_for, redirect
import os
from classify import classify
from calculations import calculate

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
    
    return redirect(url_for("results"))

@app.route("/results")
def results():
    disease = session.get("disease")
    percentage = session.get("percentage")

    return render_template("results.html", disease = disease, percentage = percentage)

@app.route("/question")
def questions():
    return redirect(url_for("home"))


@app.route("/information", methods = ["POST"])
def information():

    weight = request.form['weight']
    height = request.form['height']
    sleep = request.form['sleep']
    bPM = request.form['BPM']
    bloodPressure = request.form['bloodPressure']
    cholestoral = request.form['cholestoral']
    weight = int(weight)
    height = int(height)
    sleep = int(sleep)
    bPM = int(bPM)
    bloodPressure = int(bloodPressure)
    cholestoral = int(cholestoral)
    dict = calculate(weight,height,sleep,bPM,bloodPressure,cholestoral)

    return render_template("userInput.html", BMI = dict['BMI'], sleep = dict['sleep'], BPM = dict['BPM'], bloodPressure = dict['bloodPressure'], cholestoral = dict['cholestoral'], percentage = dict['value'])
    
    



if(__name__ == '__main__'):
    app.run(debug = True)