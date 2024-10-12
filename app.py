import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, image_parts, prompt):
    """
    Generate a response from the Gemini 1.5 Flash model.

    Args:
        input_text (str): The input string that includes user-provided information.
        image_parts (list): A list of image parts (typically containing the uploaded image).
        prompt (str): The prompt to guide the AI response.

    Returns:
        str: The generated response text from the model.
    """
    try:
        # Create a GenerativeModel instance for the specified Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        
        # Prepare the input for the model, including the text and image
        response = model.generate_content([input_text, image_parts[0], prompt])
        
        # Return the text content of the response
        return response.text
    except Exception as e:
        # Handle any exceptions and log the error
        st.error(f"Error generating response: {e}")
        return "No response generated."

def input_image_setup(uploaded_file):
    """Process the uploaded image file for input to the model."""
    if uploaded_file is not None:
        # Read the image content into bytes
        image_bytes = uploaded_file.read()
        # Create a dictionary with the file's MIME type and byte data
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": image_bytes
        }]
        return image_parts  # Return the list containing the image data
    else:
        raise FileNotFoundError("No image uploaded. Please upload a valid image.")

# Input prompt for invoice analysis
invoice_analysis_prompt = (
    "You are an expert in invoice analysis. "
    "Upon uploading an image of an invoice, please answer the following questions related to the content of the invoice:\n"
    "1. What is the total amount due?\n"
    "2. What items are listed in the invoice?\n"
    "3. What is the invoice date?\n"
    "4. Are there any payment terms mentioned?\n"
    "5. Please extract any other relevant information from the invoice.\n"
    "Make sure to accurately interpret and extract details from the uploaded invoice image."
)

# Streamlit App Layout
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction", layout="wide")
st.title("GeminiDecode: Multilanguage Document Extraction")

uploaded_file = st.file_uploader("Upload an image of a document (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        # Process the uploaded image
        image_parts = input_image_setup(uploaded_file)
        st.image(Image.open(uploaded_file), caption="Uploaded Document", use_column_width=True)

        # User input for prompt (using the predefined prompt for invoice analysis)
        user_prompt = invoice_analysis_prompt  # You can modify this to accept custom input if desired

        if st.button("Tell me about the document"):
            # Get response from Gemini 1.5 Flash
            response = get_gemini_response(user_prompt, image_parts, user_prompt)
            if response:
                st.success("Response:")
                st.write(response)
            else:
                st.warning("No response generated. Try a different prompt.")

    except Exception as e:
        st.error(f"Error processing the image: {e}")
else:
    st.info("Please upload a document to begin.")
