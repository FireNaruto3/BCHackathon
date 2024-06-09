from flask import Flask, render_template, request, session, url_for, redirect
import os
from classify import classify
from calculations import calculate
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "69420"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# OAuth configuration
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id='Ov23limDLOmSEV4hND4Q',
    client_secret='bef482caf1d4954b73c288c1557b680de0d82108',
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/auth',
    client_kwargs={'scope': 'user:email'},
)


@app.route("/")
def hello():
    return render_template("login.html")

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/auth')
def authorize():
    token = github.authorize_access_token()
    resp = github.get('https://api.github.com/user', token=token)
    user_info = resp.json()

    # Fetch emails
    emails_resp = github.get('https://api.github.com/user/emails', token=token)
    emails = emails_resp.json()

    # Select primary email if available
    primary_email = None
    for email in emails:
        if email.get('primary') and email.get('verified'):
            primary_email = email.get('email')
            break

    # Add email to user_info
    user_info['email'] = primary_email

    # Ensure 'name' key exists and fallback to 'login' if not available
    if 'name' not in user_info or not user_info['name']:
        user_info['name'] = user_info.get('login', 'Name not available')

    session['user'] = user_info

    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user)
    return redirect('/')



@app.route("/home")
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