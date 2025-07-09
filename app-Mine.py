# ===============================================
# 🔽 MODEL DOWNLOAD FROM GOOGLE DRIVE
# ===============================================

import os
import requests

MODEL_PATH = "model_blood_group_detection.h5"
GDRIVE_FILE_ID = "1Ax6p_6hNrggVAtu2EN5qjzRmOEd5T8j1"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("🔽 Downloading model from Google Drive...")
        url = f"https://drive.google.com/uc?export=download&id={GDRIVE_FILE_ID}"
        response = requests.get(url)
        with open(MODEL_PATH, 'wb') as f:
            f.write(response.content)
        print("✅ Model downloaded!")
    else:
        print("✅ Model already exists.")

download_model()

# ===============================================
# 🌐 FLASK IMPORTS & MODULES
# ===============================================

from flask import Flask, render_template, request
from markupsafe import Markup
import numpy as np
import pandas as pd

import pickle
import io
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ===============================================
# 🧠 MODEL UTILITIES
# ===============================================

disease_dic = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
from model_predict import pred_leaf_disease

# ===============================================
# 🚀 FLASK APP SETUP
# ===============================================

app = Flask(__name__)

# -----------------------------------------------
# Home Page
# -----------------------------------------------
@app.route('/')
def home():
    title = 'Blood Grouping Detection Using Image Processing'
    return render_template('index.html', title=title)

# -----------------------------------------------
# Disease Prediction Endpoint
# -----------------------------------------------
@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    title = 'Blood Grouping Detection Using Image Processing'

    if request.method == 'POST':
        file = request.files.get('file')

        img = Image.open(file)
        img.save('output.BMP')

        prediction = pred_leaf_disease("output.BMP")
        prediction = str(disease_dic[prediction])

        print("🩸 Blood group predicted:", prediction)

        precaution = prediction  # Simple assignment here

        # Fetch form details
        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        date = request.form.get('date')
        gender = request.form.get('gender')

        print(f"📝 Patient Info: {patient_id}, {patient_name}, {age}, {date}, {gender}")

        # Create PDF folder & file
        folder_name = f"{patient_name}_{patient_id}"
        os.makedirs(folder_name, exist_ok=True)

        pdf_file_name = f"{folder_name}/medical_report.pdf"
        c = canvas.Canvas(pdf_file_name, pagesize=letter)

        # Fill the PDF with patient info
        c.setFontSize(16)
        c.drawString(50, 750, "Medical Report")

        c.setFontSize(12)
        c.drawString(50, 700, f"Patient ID: {patient_id}")
        c.drawString(50, 680, f"Patient Name: {patient_name}")
        c.drawString(50, 660, f"Age: {age}")
        c.drawString(50, 640, f"Date: {date}")
        c.drawString(50, 620, f"Gender: {gender}")
        c.drawString(50, 600, f"Predicted Blood Group: {prediction}")

        c.save()

        return render_template('disease-result.html',
                               prediction=prediction,
                               precaution=precaution,
                               title=title)

    return render_template('disease.html', title=title)

# ===============================================
# 🔁 APP RUNNER
# ===============================================
if __name__ == '__main__':
    app.run(debug=True)
