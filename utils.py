import io
from PIL import Image
import numpy as np
from skimage.io import imread  # Import the imread function from skimage for image reading
import tensorflow as tf

def preprocess_image(image_file: io.BytesIO, streamlit_use=True) -> np.ndarray:
    """
    Preprocess the image for the model.

    Args:
        image_file (io.BytesIO): In-memory image file as bytes.
        streamlit_use (bool): Flag to determine if the image should be returned as a PIL Image 
                              (for Streamlit) or as a numpy array (for model prediction).

    Returns:
        np.ndarray or PIL.Image: Preprocessed image as a numpy array or PIL Image, 
                                 depending on the `streamlit_use` flag.
    """
    target_size = (480, 480)  # Define target height and width for resizing

    # Convert the BytesIO object to a byte string
    image_bytes = image_file.read()

    # Use TensorFlow to process the image
    img = tf.io.decode_image(image_bytes, channels=3)
    img = tf.image.resize(img, target_size)
    img = tf.cast(img, tf.float32) / 255.0

    if streamlit_use:
        # Convert the TensorFlow tensor back to a PIL Image for display in Streamlit
        img_numpy = img.numpy()  # Convert the tensor to a numpy array
        preprocessed_image = Image.fromarray((img_numpy * 255).astype(np.uint8))
        return preprocessed_image
    else:
        # Return the preprocessed image as a numpy array for model prediction
        return img.numpy()

def get_color_map():
    """
    Define a color map for visualizing segmentation masks.

    Returns:
        np.ndarray: Array mapping class indices to RGB colors.
    """
    return np.array([
        [0, 0, 0],       # Class 0: Black (Lunar Soil / Background)
        [255, 0, 0],     # Class 1: Red (Large Rocks)
        [0, 255, 0],     # Class 2: Green (Sky)
        [0, 0, 255]      # Class 3: Blue (Small Rocks)
        # Add more colors as needed for additional classes
    ], dtype=np.uint8)

def load_model(model_path: str):
    """
    Load a pre-trained TensorFlow model from a file.

    Args:
        model_path (str): Path to the saved model file.

    Returns:
        tf.keras.Model: Loaded TensorFlow model.
    """
    return tf.keras.models.load_model(model_path, compile=False)
