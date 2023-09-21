import streamlit as st
import subprocess

# Streamlit UI components
st.title("Text Analysis with LocalAI and k8sgpt")
st.header("Authentication")

# Authentication form
backend = st.selectbox("Select Backend", ["localai", "privateGPT"])
model_path = st.text_input("Model Path", "model/ggml-gpt4all-j")
base_url = st.text_input("Base URL", "http://localhost:8080/v1")

if st.button("Authenticate"):
    # Authenticate with k8sgpt using the selected backend
    auth_command = f"k8sgpt auth add --backend {backend} --model {model_path} --baseurl {base_url}"
    auth_result = subprocess.run(auth_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    st.write(auth_result.stdout)
    st.error(auth_result.stderr)

st.header("Text Analysis")
text_to_analyze = st.text_area("Enter Text for Analysis")

if st.button("Analyze"):
    # Analyze the text using k8sgpt with the selected backend
    analysis_command = f"k8sgpt analyze --explain --backend {backend}"
    analysis_result = subprocess.run(analysis_command, input=text_to_analyze, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)
    # Split the analysis result into lines
    analysis_lines = analysis_result.stdout.strip().split('\n')

    # Initialize a flag to track whether the first result has been displayed
    first_result_displayed = False
    # Display the header (AI Provider) and the first result
    for line in analysis_lines:
        st.write(line)
        if line.strip() == "":
            if first_result_displayed:
                break  # If the first result has already been displayed, break
            first_result_displayed = True
