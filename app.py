import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Define app sections
def calorie_health_tracker():
    st.header("Calorie Health Tracker")
    uploaded_file = st.file_uploader("Upload a food image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        input_prompt = """
            You are an expert in nutritionist where you need to see the food items from the image
            and calculate the total calories, also provide the details of every food items with calories intake
            is below format

                1. Item 1 - no of calories
                2. Item 2 - no of calories
                ----
                ----
            Finally, you can also mention if the food is healthy or not with proper reason why, 
            and also mention the percentage split of the ratio of carbohydrates, fats, fibers, sugars and
            other important information required in our diet
        """
        if st.button("Analyze Food"):
            try:
                image_data = [
                    {"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}
                ]
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([input_prompt, image_data[0]])
                st.subheader("Analysis Results")
                st.write(response.text)

                # Save to history
                st.session_state.history.append({
                    "section": "Calorie Health Tracker",
                    "result": response.text
                })

            except Exception as e:
                st.error(f"Error: {e}")

def invoice_insight_extractor():
    st.header("Invoice Insight Extractor")
    user_query = st.text_input("Enter your question about the invoice:")
    uploaded_file = st.file_uploader("Upload an invoice image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded Invoice: {uploaded_file.name}", use_container_width=True)

        if st.button("Extract and Answer"):
            try:
                input_prompt = """
                    You area an expert in understanding invoices. We will upload an image as invoice
                    and you will answer any following questions based on the uploaded invoice image
                """
                image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([input_prompt, image_data[0], user_query])
                st.subheader("Response:")
                st.write(response.text)

                # Save to history
                st.session_state.history.append({
                    "section": "Invoice Insight Extractor",
                    "question": user_query,
                    "result": response.text
                })

            except Exception as e:
                st.error(f"Error: {e}")

def image_insight_extraction():
    st.header("Image Insight Extraction")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        input_prompt = """
            You are an expert AI trained in visual and contextual analysis. Your task is to analyze the uploaded image and provide a detailed description.

            1. Identify if the image is from a movie poster or any popular media. If yes, provide the name of the movie or media.
            2. Describe the visual elements of the image, such as objects, characters, or text visible.
            3. Mention any specific stylistic or artistic details that help identify the context of the image.
            4. If possible, recognize any iconic symbols, logos, or designs in the image and explain their significance.
            5. Provide a concise summary of what the image represents.

            Be as detailed and accurate as possible in your response.
        """
        if st.button("Get Insights"):
            try:
                image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([input_prompt, image_data[0]])
                st.subheader("Image Analysis Results")
                st.write(response.text)

                # Save to history
                st.session_state.history.append({
                    "section": "Image Insight Extraction",
                    "result": response.text
                })

            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar navigation with dynamic highlighting
st.set_page_config(page_title="Multi-Functional App", layout="wide")

if "selected" not in st.session_state:
    st.session_state.selected = "Calorie Health Tracker"

sidebar_options = {
    "Calorie Health Tracker": calorie_health_tracker,
    "Invoice Insight Extractor": invoice_insight_extractor,
    "Image Insight Extraction": image_insight_extraction,
}

# Inject custom CSS for styling sidebar buttons and centering the title
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        width: 100%;
    }
    .stSidebarTitle {
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 10px;
    }
    .stButton button {
        width: 100%;
        background-color: #f9f9f9;
        border: 2px solid #dcdcdc;
        border-radius: 6px;
        color: black;
        text-align: left;
        padding: 10px;
        font-size: 16px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #e0e4eb;
        border-color: #c0c0c0;
    }
    .stButton.active button {
        background-color: #1e90ff;
        color: white;
        border-color: #1c86ee;
    }
    </style>
""", unsafe_allow_html=True)

# Render centered title and sidebar buttons
st.sidebar.markdown('<div class="stSidebarTitle">Navigation</div>', unsafe_allow_html=True)
for option in sidebar_options.keys():
    is_active = st.session_state.selected == option
    button_style = "active" if is_active else ""
    if st.sidebar.button(option, key=option):
        st.session_state.selected = option

# Apply dynamic highlighting and render the selected app
selected_app = st.session_state.selected
st.sidebar.markdown(f"**Currently  Active:** {selected_app}")
sidebar_options[selected_app]()

# Display history
st.sidebar.markdown("---")
st.sidebar.markdown("### History")
with st.sidebar.expander("View Session History"):
    for entry in st.session_state.history:
        st.markdown(f"**Section:** {entry['section']}")
        if "question" in entry:
            st.markdown(f"**Question:** {entry['question']}")
        st.markdown(f"**Result:** {entry['result']}")
        st.markdown("---")

