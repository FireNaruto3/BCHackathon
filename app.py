from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/eyeDisease.html")
def test():
    return render_template("eyeDisease.html")

if(__name__ == '__main__'):
    app.run(debug = True)