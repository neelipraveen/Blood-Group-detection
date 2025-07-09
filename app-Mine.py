# Importing essential libraries and modules

from flask import Flask, render_template, request
from markupsafe import Markup
import numpy as np
import pandas as pd

import requests
import config
import pickle
import io
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading plant disease classification model

disease_dic= ['A+','A-', 'AB+', 'AB-','B+','B-','O+','O-']



from model_predict  import pred_leaf_disease

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


app = Flask(__name__)

# render home page


@ app.route('/')
def home():
    title = 'Blood Grouping Detection Using Image Processing'
    return render_template('index.html', title=title)

# render crop recommendation form page

@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    title = 'Blood Grouping Detection Using Image Processing'

    if request.method == 'POST':
        #if 'file' not in request.files:
         #   return redirect(request.url)

            file = request.files.get('file')

           # if not file:
            #    return render_template('disease.html', title=title)

            img = Image.open(file)
            img.save('output.BMP')


            prediction =pred_leaf_disease("output.BMP")

            prediction = (str(disease_dic[prediction]))

            print("print the blood group of the candidate ",prediction)
#disease_dic= ['A-','A+', 'AB-','AB+', 'B-','B+','O-','O+']
            if prediction=='A-':
                     precaution='A-'
 
            elif prediction=='A+':

                    precaution='A+'
            elif prediction=='AB-':

                   precaution='AB-'
            elif prediction=='AB+':

                   precaution='AB+'
            elif prediction=='B-':

                   precaution='B-'
            elif prediction=='B+':

                   precaution='B+'
            elif prediction=='O-':

                   precaution='O-'
            elif prediction=='O+':

                   precaution='O+'


            patient_id = request.form.get('patient_id')
            patient_name = request.form.get('patient_name')
            age = request.form.get('age')
            date = request.form.get('date')
            gender = request.form.get('gender')

            print(patient_id,patient_name,age,date,gender)
                    
        # Your code to process the uploaded image and text inputs goes here

    #return render_template('disease.html', title=title)

            # Set up the canvas and page size

            import os

            # Create a folder with the patient name and ID11
            folder_name = f"{patient_name}_{patient_id}"
            os.makedirs(folder_name, exist_ok=True)

            # Set up the canvas and page size
            pdf_file_name = f"{folder_name}/medical_report.pdf"
            c = canvas.Canvas(pdf_file_name, pagesize=letter)

 #           c = canvas.Canvas("medical_report.pdf", pagesize=letter)

            # Define the patient data
            #patient_id = '1232'
            #patient_name = 'Ravi'
            #age = '24'
            #date = '1898-12-11'
            #gender = 'male'
            skin_cancer = prediction

            # Write the report title
            c.setFontSize(16)
            c.drawString(50, 750, "Medical Report")

            # Write the patient information
            c.setFontSize(12)
            c.drawString(50, 700, "Patient ID: " + patient_id)
            c.drawString(50, 680, "Patient Name: " + patient_name)
            c.drawString(50, 660, "Age: " + age)
            c.drawString(50, 640, "Date: " + date)
            c.drawString(50, 620, "Gender: " + gender)
            c.drawString(50, 600, "Abnormal ECG is: " + skin_cancer)

            # Save the PDF file
            c.save()

            return render_template('disease-result.html', prediction=prediction,precaution=precaution,title=title)
        #except:
         #   pass
    return render_template('disease.html', title=title)


# render disease prediction result page


# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=True)
