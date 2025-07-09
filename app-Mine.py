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

from flask import Flask, render_template, request, send_file
from markupsafe import Markup
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

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
        img = Image.open(file).convert('RGB')

        # Form data
        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        date = request.form.get('date')
        gender = request.form.get('gender')
        safe_name = patient_name.replace(" ", "_")

        # Prediction
        img.save('output.BMP')  # for prediction
        prediction = pred_leaf_disease("output.BMP")
        prediction = str(disease_dic[prediction])
        precaution = prediction

        print(f"🩸 Blood Group: {prediction}")
        print(f"📝 Patient: {patient_id}, {patient_name}, {age}, {date}, {gender}")

        # Generate dynamic PDF filename
        safe_name = patient_name.replace(" ", "_")
        pdf_filename = f"medical_report_{safe_name}.pdf"
        pdf_path = os.path.join(folder_name, pdf_filename)

        # Create PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFontSize(16)
        c.drawString(50, 750, "Medical Report")
        c.setFontSize(12)
        c.drawString(50, 700, f"Patient ID: {patient_id}")
        c.drawString(50, 680, f"Patient Name: {patient_name}")
        c.drawString(50, 660, f"Age: {age}")
        c.drawString(50, 640, f"Date: {date}")
        c.drawString(50, 620, f"Gender: {gender}")
        c.drawString(50, 600, f"Predicted Blood Group: {prediction}")

        # Insert image in PDF
        try:
            c.drawImage(image_path, 350, 600, width=150, height=150)
        except Exception as e:
            print("⚠️ Failed to embed image:", e)

        c.save()

        # Send PDF to client
        pdf_buffer.seek(0)
        return send_file(pdf_buffer,
                         as_attachment=True,
                         download_name=f"medical_report_{safe_name}.pdf",
                         mimetype='application/pdf')

    return render_template('disease.html', title=title)

# -----------------------------------------------
# Manual Report Download Endpoint (Legacy)
# -----------------------------------------------
@app.route('/download-report/<folder_name>/<pdf_file>')
def download_report(folder_name, pdf_file):
    file_path = os.path.join(folder_name, pdf_file)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Report not found", 404

# ===============================================
# 🔁 APP RUNNER
# ===============================================
if __name__ == '__main__':
    app.run(debug=True)
