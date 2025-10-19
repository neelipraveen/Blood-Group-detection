import os
import requests
from flask import Flask, render_template, request, send_file
from markupsafe import Markup
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ===============================================
# 🔽 MODEL DOWNLOAD FROM GOOGLE DRIVE
# ===============================================
MODEL_PATH = "New_final_save.h5"
GDRIVE_FILE_ID = "1FDqoLJwv249YW-W1eaxQoxKj4pCaY67y"

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

        # --- NEW: Check for file and file type ---
        if not file or not file.filename:
            error_message = "No file was uploaded. Please select a file."
            return render_template('disease.html', title=title, error=error_message)

        if not file.filename.lower().endswith('.bmp'):
            error_message = "Invalid fingerprint image. Please upload a .BMP file."
            return render_template('disease.html', title=title, error=error_message)
        # --- End of new code ---

        # If the file is valid, proceed as before
        img = Image.open(file).convert('RGB')

        # Save temp image for prediction
        temp_image_path = 'temp_uploaded_image.BMP'
        img.save(temp_image_path)

        # Predict blood group
        prediction_index = pred_leaf_disease(temp_image_path)
        prediction = str(disease_dic[prediction_index])
        precaution = prediction

        # Form data
        patient_id = request.form.get('patient_id') or "UnknownID"
        patient_name = request.form.get('patient_name') or "UnknownName"
        age = request.form.get('age') or "N/A"
        date = request.form.get('date') or "N/A"
        gender = request.form.get('gender') or "N/A"
        safe_name = patient_name.replace(" ", "_")

        print(f"🩸 Blood Group: {prediction}")
        print(f"📝 Patient: {patient_id}, {patient_name}, {age}, {date}, {gender}")

        # Folder + file setup
        folder_name = f"{safe_name}_{patient_id}"
        os.makedirs(folder_name, exist_ok=True)
        pdf_file = f"medical_report_{safe_name}.pdf"
        pdf_path = os.path.join(folder_name, pdf_file)

        # Create and save PDF
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

        try:
            c.drawImage(temp_image_path, 350, 600, width=150, height=150)
        except Exception as e:
            print("⚠️ Failed to embed image in PDF:", e)

        c.save()
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        # Pass info to result page
        return render_template(
            'disease-result.html',
            title=title,
            prediction=prediction,
            precaution=precaution,
            folder_name=folder_name,
            pdf_file=pdf_file
        )

    return render_template('disease.html', title=title)

# -----------------------------------------------
# Manual PDF Download Endpoint
# -----------------------------------------------
@app.route('/download-report/<folder_name>/<pdf_file>')
def download_report(folder_name, pdf_file):
    file_path = os.path.join(folder_name, pdf_file)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "❌ Report not found", 404

# ===============================================
# 🔁 APP RUNNER
# ===============================================
if __name__ == '__main__':
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

