import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# openai.api_key = st.secrets["api_key"]
# Initialize Computer Vision Client
computervision_client = ComputerVisionClient('https://cvdrlee.cognitiveservices.azure.com/', CognitiveServicesCredentials(st.secrets["az_key"]))

def analyze_image(image):
    # Convert image to bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Analyze the image
    analysis = computervision_client.analyze_image_in_stream(img_byte_arr, visual_features=["Categories", "Tags", "Description", "Color", "ImageType"])
    
    # Return the analysis results
    return analysis

def display_analysis(analysis):
    st.write("### Categories:")
    for category in analysis.categories:
        st.write(f"  {category.name} ({category.score*100:.2f}%)")

    st.write("### Tags:")
    for tag in analysis.tags:
        st.write(f"  {tag.name} ({tag.confidence*100:.2f}%)")

    st.write("### Description:")
    st.write(f"  {analysis.description.captions[0].text} (Confidence: {analysis.description.captions[0].confidence*100:.2f}%)")

    st.write("### Dominant Color Foreground:", analysis.color.dominant_color_foreground)
    st.write("### Dominant Color Background:", analysis.color.dominant_color_background)

    st.write("### Image Type:")
    st.write(f"  Clip Art Type: {analysis.image_type.clip_art_type}")
    st.write(f"  Line Drawing Type: {analysis.image_type.line_drawing_type}")

st.title('Azure Computer Vision App')

# Upload image through file uploader
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])

# Or enter image URL
url = st.text_input("Or enter Image URL:")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    analysis = analyze_image(image)
    display_analysis(analysis)
elif url:
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption='Image from URL.', use_column_width=True)
        st.write("")
        st.write("Classifying...")
        analysis = analyze_image(image)
        display_analysis(analysis)
    except Exception as e:
        st.write("Invalid URL or the URL does not point to an image.")

