import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.models import load_model

# Load the model once globally
loaded_model_imageNet = load_model("New_final_save.h5")

def pred_leaf_disease(image_path: str) -> int:
    """
    Predicts the blood group from an image path using the pre-trained model.

    Args:
        image_path (str): Path to the image file.

    Returns:
        int: Index of the predicted class (0-7 for 8 blood groups).
    """
    try:
        # Load and preprocess the image
        img = image.load_img(image_path, target_size=(256, 256))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predict
        result = loaded_model_imageNet.predict(x)
        result_percent = (result * 100).astype(int)
        print("🔍 Prediction result (percent):", result_percent)

        # Return the index of the max confidence score
        return int(np.argmax(result_percent[0]))

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return -1
