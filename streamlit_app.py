import streamlit as st
import subprocess

# Streamlit UI components
st.title("K8SGPT Analysis with LocalAI")
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

# Resource analysis section
st.header("Resource Analysis")

# Define a dictionary to map user-friendly resource names to k8sgpt filter values
resource_mapping = {
    "Pod": "Pod",
    "VulnerabilityReport": "VulnerabilityReport",
    "Deployment": "Deployment",
    "Service": "Service",
    "StatefulSet": "StatefulSet",
    "ReplicaSet": "ReplicaSet",
    "PersistentVolumeClaim": "PersistentVolumeClaim",
    "Ingress": "Ingress",
    "CronJob": "CronJob",
    "Node": "Node",
    "NetworkPolicy": "NetworkPolicy",
    "HorizontalPodAutoScaler": "HorizontalPodAutoScaler",
    "PodDisruptionBudget": "PodDisruptionBudget"
}

# User input: Select resource type
selected_resource = st.selectbox("Select Resource Type", list(resource_mapping.keys()))

# Get the corresponding k8sgpt filter value
selected_filter = resource_mapping.get(selected_resource)

# Execute k8sgpt commands based on user input
if selected_filter:
    st.subheader(f"Analysis Output: {selected_resource}s")

    # k8sgpt commands
    analyze_command = f"k8sgpt analyze --explain --filter={selected_filter} --backend={backend}"
    analyze_result = subprocess.run(analyze_command, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True)
    st.code(analyze_result.stdout, language="bash")
    st.error(analyze_result.stderr)
else:
    st.warning("Please select a valid resource type.")
