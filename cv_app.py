import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

az_key = st.secrets["az_key"]
# Initialize Computer Vision Client
computervision_client = ComputerVisionClient('https://cvdrlee.cognitiveservices.azure.com/', CognitiveServicesCredentials(az_key))

def analyze_image(image):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    
    # Reset the pointer of BytesIO object to the start
    img_byte_arr.seek(0)
    
    # Use BytesIO object directly as it's a type of stream
    analysis = computervision_client.analyze_image_in_stream(img_byte_arr, visual_features=["Categories", "Tags", "Description", "Color", "ImageType"])
    
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

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])
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
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Image from URL.', use_column_width=True)
            st.write("")
            st.write("Classifying...")
            analysis = analyze_image(image)
            display_analysis(analysis)
        else:
            st.error("The URL does not point to a valid image. Content-Type received was " + content_type)
            
    except requests.RequestException as e:
        st.error(f"Failed to fetch image due to request exception: {str(e)}")
        
    except requests.HTTPError as e:
        st.error(f"HTTP Error occurred: {str(e)}")
        
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
