import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np

# If you have an existing 'api_clients.py' with your real detection logic, import it:
from api_clients import analyze_media, generate_insights, fact_check_info

# -------------------------------------------------
# Page configuration (kept in the same place):
# -------------------------------------------------
st.set_page_config(page_title="DeepFake Detection", layout="centered")

# -------------------------------------------------
# Animated Gradient Background & Button Hover (CSS)
# -------------------------------------------------
st.markdown("""
<style>
/* Animate a gradient background across the entire page */
@keyframes gradientBG {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
body {
    background: linear-gradient(90deg, #ff8a00, #da1b60);
    background-size: 200% 200%;
    animation: gradientBG 10s ease infinite;
    color: #ffffff !important;
    margin: 0;
    padding: 0;
}

/* Fade in images for a smoother appearance */
img {
    animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* Scale buttons on hover */
div[data-testid="stButton"] > button:hover {
    transform: scale(1.05);
    transition: transform 0.2s;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# App Title & Description
# -------------------------------------------------
st.title("DeepFake Detection with Groq & Prepexitiy")
st.write("""
Upload images or videos to detect deepfakes. 
Now, each upload also trains (or updates) the AI model with the newly provided data. 
(This is a demo feature—real-time training can be resource-intensive in production.)
""")

# -------------------------------------------------
# Additional Verification (Placeholder)
# -------------------------------------------------
def additional_verification(detection_result):
    """
    Example: Provide extra scrutiny or caution messages 
    after the main deepfake detection is done.
    """
    classification = detection_result.get("classification", "")
    confidence = detection_result.get("confidence", 0)

    try:
        confidence = float(confidence)
    except ValueError:
        confidence = 0.0

    if classification == "Deepfake Detected" and confidence > 0.8:
        return "Warning: High-confidence deepfake. Extra scrutiny recommended."
    elif classification == "Deepfake Detected":
        return "Medium confidence deepfake. Further manual review suggested."
    else:
        return "No additional issues found."

# -------------------------------------------------
# Placeholder: Integrate Groq & Prepexitiy
# -------------------------------------------------
def analyze_with_groq_and_prepexitiy(media_data, file_type):
    """
    Demonstrates how you might integrate Groq (hardware) 
    and Prepexitiy (software) for deepfake detection.
    
    Currently, we simply call `analyze_media` from your existing logic,
    but in a real scenario, you’d replace this with actual integration code.
    """
    detection_result = analyze_media(media_data, file_type=file_type)
    return detection_result

# -------------------------------------------------
# New: Train/Update the AI Model
# -------------------------------------------------
def train_ai_model(media_data, detection_result):
    """
    Placeholder function to illustrate how you might train or update 
    your model with newly uploaded data. 
    
    In a real scenario, you'd:
      1) Determine if the media is labeled (e.g., 'Deepfake' or 'Authentic').
      2) Convert the file to a suitable format for training.
      3) Update or retrain your model (incremental or offline).
    
    For this hackathon demo, we just return a message.
    """
    classification = detection_result.get("classification", "Unknown")
    confidence = detection_result.get("confidence", "N/A")

    # Example: Log or store the data somewhere
    # For now, we simply return a placeholder string.
    return f"Model updated with new data labeled '{classification}' (confidence: {confidence})."

# -------------------------------------------------
# File Uploader for Deepfake Detection
# -------------------------------------------------
uploaded_file = st.file_uploader("Choose an image or video file", 
                                 type=["jpg", "jpeg", "png", "mp4", "mov"])

if uploaded_file:
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type}
    st.write(file_details)

    # Process the file
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        media_data = img_byte_arr.getvalue()
    elif uploaded_file.type.startswith("video"):
        video_bytes = uploaded_file.read()
        nparr = np.frombuffer(video_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is not None:
            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 
                     caption="Video Preview", 
                     use_column_width=True)
        else:
            st.write("Could not extract preview frame.")
        media_data = video_bytes

    # -------------------------------------------------
    # Analyze Media (Using Groq & Prepexitiy Placeholder)
    # -------------------------------------------------
    with st.spinner("Analyzing media for deepfakes..."):
        detection_result = analyze_with_groq_and_prepexitiy(media_data, 
                                                            file_type=uploaded_file.type)

    st.subheader("DeepFake Detection Result")
    if "error" in detection_result:
        st.error(detection_result["error"])
    else:
        st.write("**Classification:**", detection_result.get("classification"))
        st.write("**Confidence Score:**", detection_result.get("confidence"))
        st.write("**Full Details:**", detection_result)

        # If deepfake is detected, generate insights and optionally fact-check
        if detection_result.get("classification") == "Deepfake Detected":
            with st.spinner("Generating insights..."):
                insights = generate_insights(detection_result)
            st.subheader("Insights")
            st.write(insights)

            # If your detection logic extracts claims, you can fact-check them
            if detection_result.get("claims"):
                with st.spinner("Verifying claims..."):
                    fact_check_results = fact_check_info(detection_result["claims"])
                st.subheader("Fact Check Results")
                st.write(fact_check_results)
        else:
            st.success("No deepfake signs detected!")

        # -------------------------------------------------
        # Additional Verification
        # -------------------------------------------------
        with st.spinner("Performing additional verification..."):
            extra_check = additional_verification(detection_result)
        st.subheader("Additional Verification")
        st.write(extra_check)

        # -------------------------------------------------
        # Train/Update Model with New Data
        # -------------------------------------------------
        with st.spinner("Updating AI model with newly uploaded data..."):
            training_result = train_ai_model(media_data, detection_result)
        st.subheader("Model Training")
        st.write(training_result)
