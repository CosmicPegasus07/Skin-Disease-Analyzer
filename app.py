import os
import numpy as np
import uuid
import flask
import urllib
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array
import cv2

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'Models/vgg19byzeeza.h5'))

ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

def predict(filename , model):
    classes = ['Acne','Actnic Cheilitis','Basal Cell Carcinoma','Eczema Photos','Hair Disease','Nail Fungal','Psoriasis Hair','Rosacea',' Scabies',' Seborrheic Keratoses','Skin Cancer','Tinea Ringworm Candidiasis','Warts Molluscum']
    img = cv2.resize(cv2.imread(filename), (32,32)) / 255.0
    prediction = model.predict(img.reshape(1,32,32,3))
    return classes[np.argmax(prediction)]

@app.route('/')
def home():
        return render_template("index.html")

@app.route('/check')
def check():
        return render_template("check.html")

@app.route('/rem')
def remedies():
        return render_template("rem.html")

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static/uploads')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img , filename)
                output = open(img_path , "wb")
                output.write(resource.read())
                output.close()
                img = filename

                class_result = predict(img_path , model)

            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , class_result = class_result)
            else:
                return render_template('index.html' , error = error) 

            
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                class_result = predict(img_path , model)


            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , class_result = class_result)
            else:
                return render_template('index.html' , error = error)

    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(debug = True)
