# # from flask import Flask, redirect, url_for, render_template
# # from classify import classify
# # import os
# # from werkzeug.utils import secure_filename

# # app = Flask(__name__)

# # @app.route("/")
# # def home():
# #     return render_template("index.html")

# # @app.route("/eyeDisease.html")
# # def test():
# #     return render_template("eyeDisease.html")

# # if(__name__ == '__main__'):
# #     app.run(debug = True)

# # UPLOAD_FOLDER = 'uploads'
# # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # if not os.path.exists(UPLOAD_FOLDER):
# #     os.makedirs(UPLOAD_FOLDER)

# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # @app.route('/', methods=['GET', 'POST'])
# # def upload_file():
# #     if request.method == 'POST':
# #         if 'file' not in request.files:
# #             return redirect(request.url)
# #         file = request.files['file']
# #         if file.filename == '':
# #             return redirect(request.url)
# #         if file and allowed_file(file.filename):
# #             filename = secure_filename(file.filename)
# #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #             file.save(filepath)
# #             predicted_class_name, confidence = classify(filepath)
# #             result = {
# #                 'predicted_class_name': predicted_class_name,
# #                 'confidence': confidence
# #             }
# #             return render_template('index.html', result=result)
# #     return render_template('index.html', result=None)

# # if __name__ == '__main__':
# #     app.run(debug=True)

# from flask import Flask, request, render_template, redirect, url_for
# import os
# from werkzeug.utils import secure_filename
# from classify import classify

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             predicted_class_name, confidence = classify(filepath)
#             result = {
#                 'predicted_class_name': predicted_class_name,
#                 'confidence': confidence
#             }
#             return render_template('index.html', result=result)
#     return render_template('index.html', result=None)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import os
# import classify.classify as classify
from classify import classify


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
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return 'No selected file'
    
        # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return classify(file_path)
    # return f'File uploaded successfully. Saved at: {file_path}'



if(__name__ == '__main__'):
    app.run(debug = True)