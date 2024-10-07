import streamlit as st
import requests

# Function to send data to Langflow
def send_to_langflow(id_number, svc_document):
    langflow_url = "http://localhost:8000/process"  # Replace with your Langflow endpoint

    # Prepare the files and data payload
    files = {'svc_document': svc_document}
    data = {'id_number': id_number}

    # Make the request to Langflow
    response = requests.post(langflow_url, data=data, files=files)

    if response.status_code == 200:
        return response.content
    else:
        st.error("Failed to process the document with Langflow.")
        return None

# Streamlit UI
st.title("Check Questions & Answers")

# Input Fields
id_number = st.text_input("Enter Bot ID Number:")
svc_document = st.file_uploader("Upload SVC Document", type=["svc"]) 

# Activate Button
if st.button("Submit"):
    if id_number and svc_document is not None:
        response_content = send_to_langflow(id_number, svc_document)
        
        if response_content:
            # Save the response to a file to make it available for download
            with open("processed_document.txt", "wb") as f:
                f.write(response_content)
                
            st.session_state['document_ready'] = True
            st.success("Processing completed. Download your file below.")
        else:
            st.error("Processing failed. Please try again.")
    else:
        st.warning("Please enter both an ID number and upload an SVC document.")

# Download Button
if st.session_state.get('document_ready', False):
    with open("processed_document.txt", "rb") as file:
        st.download_button(label="Download Processed Document",
                           data=file,
                           file_name="processed_document.txt",
                           mime="text/plain")
