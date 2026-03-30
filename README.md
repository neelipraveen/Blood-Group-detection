<div align="center">
  
  # Blood Group Detection from Fingerprints 🩸

  <p align="center">
    A Deep Learning and Image Processing framework designed to automatically classify human blood types (A, B, AB, O, and Rh factor) from slide agglutination tests, reducing manual diagnostic errors and accelerating clinical workflows.
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
    <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
  </p>
</div>

---

## 📖 Table of Contents
- [Project Overview](#-project-overview)
- [System Architecture](#-system-architecture)
- [Methodology](#-methodology)
- [Results & Performance](#-results--performance)
- [Quick Start](#-quick-start)

---

## 🚀 Project Overview

Determining a patient's blood group quickly and accurately is critical in emergency medicine and blood transfusions. Traditional manual observation of slide agglutination (clumping of red blood cells when reacting with specific antibodies) is prone to human error and fatigue. 

This project digitizes and automates the diagnostic process. By leveraging Computer Vision (OpenCV) and Convolutional Neural Networks (CNNs), the system analyzes microscopic or macroscopic images of blood samples reacting with Anti-A, Anti-B, and Anti-D (Rh) reagents to instantly output the correct blood type.

---

## 🧠 Methodology

1. **Image Acquisition & Preprocessing:**
   * Raw images of agglutination slides are ingested.
   * **OpenCV** is utilized for grayscale conversion, adaptive thresholding, and morphological operations (erosion/dilation) to isolate the blood sample regions from the background.
2. **Feature Extraction:**
   * The pipeline identifies granular textures and clump formations that indicate a positive antigen-antibody reaction.
3. **Deep Learning Classification (CNN):**
   * A tailored Convolutional Neural Network processes the isolated regions.
   * The model outputs a multi-label classification dictating the presence of A, B, and Rh antigens, seamlessly mapping them to the standard ABO blood group system.

---

## 📊 Results & Performance

The automated system demonstrates high diagnostic reliability, successfully distinguishing between smooth blood pools (negative reaction) and agglutinated clusters (positive reaction).

* **Model:** CNN / Custom Classifier
* **Target Output:** A+, A-, B+, B-, AB+, AB-, O+, O-

<div align="center">
  <img src="path/to/your/prediction_results_image.png" alt="Sample Detection Output" width="600"/>
  <br/>
  <i>Figure 2: Model correctly identifying agglutination for an AB+ sample.</i>
</div>

---

## 💻 Quick Start

### Prerequisites
* Python 3.9+
* OpenCV (`cv2`)
* TensorFlow / Keras
* NumPy & Matplotlib

   ```bash
   git clone [https://github.com/neelipraveen/Blood-Group-detection.git](https://github.com/neelipraveen/Blood-Group-detection.git)
   cd Blood-Group-detection
