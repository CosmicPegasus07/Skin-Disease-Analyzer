import os
import numpy as np
import uuid
import flask
import urllib
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, send_file
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR, 'Models/skin_disease_model.h5'))

ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT


def predict(filename, model):
    classes = ['Acne On Body', 'Acne On Face', 'Acne On Forehead', 'Actinic Cheilitis',
               'Alopecia Areata', 'Eczema Foot', 'Nail Fungal', 'Nose Rosacea', 'Raynauds Phenomenon']
    img = cv2.resize(cv2.imread(filename), (32, 32)) / 255.0
    prediction = model.predict(img.reshape(1, 32, 32, 3))
    return classes[np.argmax(prediction)]


@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/check')
def check():
    return render_template("check.html")

@app.route('/disease')
def disease():
    return render_template("disease.html")

@app.route('/aa')
def aa():
    return render_template("diseases/aa.html")


@app.route('/ac')
def ac():
    return render_template("diseases/ac.html")


@app.route('/aob')
def aob():
    return render_template("diseases/aob.html")


@app.route('/aof')
def aof():
    return render_template("diseases/aof.html")


@app.route('/aofh')
def aofh():
    return render_template("diseases/aofh.html")


@app.route('/ef')
def ef():
    return render_template("diseases/ef.html")


@app.route('/nf')
def nf():
    return render_template("diseases/nf.html")


@app.route('/nr')
def nr():
    return render_template("diseases/nr.html")


@app.route('/rp')
def rp():
    return render_template("diseases/rp.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/success', methods=['GET', 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/uploads')
    if request.method == 'POST':
        if (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                img = file.filename

                class_result = predict(img_path, model)
            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if (len(error) == 0):
                return render_template('success.html', img=img, class_result=class_result)
            else:
                return render_template('index.html', error=error)

    else:
        return render_template('index.html')
