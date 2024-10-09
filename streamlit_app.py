import streamlit as st
import pandas as pd
from io import StringIO
import json
import requests
from api.langflow_script import run_flow
from typing import Optional

# Streamlit UI setup
st.title("Langflow Document Processor")

# Input field for Bot ID
bot_id = st.text_input("Enter Bot ID Number:")

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload your CSV document", type=["csv"])

# Function to call Langflow API
def run_flow(message: str, endpoint: str, tweaks: dict = None, api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.
    """
    BASE_API_URL = "https://langflow-fe-jeen.delightfulwater-ecb5056f.westeurope.azurecontainerapps.io"
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks
    headers = None
    if api_key:
        headers = {"x-api-key": api_key}

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Function to process the document and call the Langflow API
def process_and_run_flow(bot_id, document_content):
    message = "Processing uploaded CSV document"
    
    # Create tweaks with the document content and bot_id
    tweaks = {
        "JeenAssistantTriggerComponentChainRequests-RyHsl": {
            "bot_id": bot_id,
            "input_value": document_content,
            "apiKey": "JeenBVZZouiaEyM03xc4EEONhPsukfHZSMBVe7IkOBoZDLesgz4Az5Zc6Ueflc5nlTyG4252UWQ3hXUELH1vOKII9x81h6zPayh2cjqXEPkWMLC2iU6PoBJ2wXmrQZ71",
            "app_name_aux": "Langflow",
            "backend_host": "https://playground-gekoo-client-test.azurewebsites.net",
            "strList": [],
            "token": ""
        }
    }

    # Call the Langflow API
    return run_flow(message=message, endpoint=bot_id, tweaks=tweaks)

# Process the file when the user clicks the "Submit" button
if st.button("Submit"):
    if bot_id and uploaded_file:
        try:
            # Read the CSV file content
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            document_content = stringio.read()

            # Run the Langflow flow with the bot ID and document content
            response = process_and_run_flow(bot_id, document_content)

            # Display the response from the Langflow API
            st.write("Langflow API Response:")
            st.json(response)

            # Save response to a JSON file for download
            response_file_path = "langflow_response.json"
            with open(response_file_path, "w") as file:
                json.dump(response, file, indent=2)

            # Provide a download button for the response
            with open(response_file_path, "rb") as file:
                st.download_button(
                    label="Download Processed Response",
                    data=file,
                    file_name="langflow_response.json",
                    mime="application/json"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid Bot ID and upload a CSV file.")
else:
    st.info("Enter the Bot ID, upload a CSV file, then click Submit to proceed.")
