from PIL import Image
import io
import streamlit as st
import requests
from utils import preprocess_image

# Set title for the tab and icon for the same
st.set_page_config(page_title = "Segment Moon", page_icon = ":moon:")

# URL of your FastAPI backend endpoint for image segmentation
FASTAPI_URL = "http://localhost:8000/segment/"
# Inject custom CSS for an animated background
st.markdown(
    f"""
    <style>
    .full-page-background {{
        background-image: url('https://static.vecteezy.com/system/resources/thumbnails/031/411/730/small_2x/ai-generated-ai-generative-evening-night-nature-outdoor-landscape-background-full-moon-and-mountains-graphic-art-photo.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
 
    }}

   
    </style>

    <div class="full-page-background"></div>
    """,
    unsafe_allow_html=True
)


# Streamlit application setup
st.title("Image Segmentation App")

# File uploader widget to allow users to upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Convert the uploaded file into an in-memory bytes object
    image_bytes = io.BytesIO(uploaded_file.read())
    
    try:
        # Preprocess the uploaded image using the custom preprocessing function
        # If streamlit_use=True, it assumes that preprocessing is tailored for Streamlit
        preprocessed_image = preprocess_image(image_bytes, streamlit_use=True)
        
        # Display the preprocessed image in the Streamlit app
        st.image(preprocessed_image, caption="Preprocessed Image", use_column_width=True)

        # Button to trigger the segmentation process
        if st.button("Segment Image"):
            # Convert the preprocessed image to bytes for sending in the POST request
            preprocessed_image_bytes = io.BytesIO()
            preprocessed_image.save(preprocessed_image_bytes, format="PNG")
            preprocessed_image_bytes.seek(0)
            
            # Prepare the file to send in the POST request
            files = {"file": ("preprocessed_image.png", preprocessed_image_bytes, "image/png")}
            
            # Send a POST request to the FastAPI backend with the preprocessed image
            response = requests.post(FASTAPI_URL, files=files)
            
            if response.status_code == 200:
                # If the request is successful, display the segmented image returned by the backend
                result_image = Image.open(io.BytesIO(response.content))
                st.image(result_image, caption="Segmented Image", use_column_width=True)
            else:
                # If there's an error, display an error message
                st.error("Error: Unable to process the image. Please try again.")
    
    except ValueError as e:
        # Display error message if preprocessing fails
        st.error(f"Error: {e}")