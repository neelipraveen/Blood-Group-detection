import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.models import load_model
from PIL import Image

# Load the model once globally
loaded_model_imageNet = load_model("model_blood_group_detection.h5")

def pred_leaf_disease(image_path):				 
    # Load image and preprocess
    img = image.load_img(image_path, target_size=(256, 256))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Predict
    result = loaded_model_imageNet.predict(x)
    result_percent = (result * 100).astype('int')
    
    print("🔍 Prediction result (percent):", result_percent)

    # Get max value index (class)
    list_vals = list(result_percent[0])
    result_val = max(list_vals)
    index_result = list_vals.index(result_val)

    return index_result
