import streamlit as st
import pandas as pd
import requests
import json
import ast

def send_to_api(text, bot_id):
    url = "https://langflow-fe-jeen.delightfulwater-ecb5056f.westeurope.azurecontainerapps.io/api/v1/run/38119a37-38a5-4566-810c-4ac486f0c7be?stream=false"
    payload = {
        "input_value": text,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "CustomComponent-Mc9Bb": {
                "backend_host": "https://playground-gekoo-client-test.azurewebsites.net"
            },
            "ParseData-FiFMM": {
                "sep": "\n",
                "template": "{token}"
            },
            "ParseData-PciqQ": {
                "sep": "\n",
                "template": "{data}"
            },
            "JeenAssistantTriggerComponentChainRequests-RyHsl": {
                "apiKey": "JeenBVZZouiaEyM03xc4EEONhPsukfHZSMBVe7IkOBoZDLesgz4Az5Zc6Ueflc5nlTyG4252UWQ3hXUELH1vOKII9x81h6zPayh2cjqXEPkWMLC2iU6PoBJ2wXmrQZ71",
                "app_name_aux": "Langflow",
                "backend_host": "https://playground-gekoo-client-test.azurewebsites.net",
                "bot_id": bot_id,
                "strList": [],
                "token": ""
            },
            "ChatOutput-rJKBM": {
                "data_template": "{text}",
                "sender": "Machine",
                "sender_name": "AI",
                "session_id": "",
                "should_store_message": True
            },
            "CustomComponent-BJz55": {},
            "ParseData-lwUUv": {
                "sep": "\n",
                "template": "{data}"
            }
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Raw API response:", response.text)
    return response.json()

def extract_text_from_json(json_data):
    try:
        output = json_data.get('outputs', [])
        if output:
            message_data = output[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('data', {}).get('text', '')
            if message_data:
                message_data = ast.literal_eval(message_data)
                value = message_data.get('value', 'Value not found')
                formatted_text = value.replace('\n', '\n\n')
                return formatted_text
        return "No output found in the response."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

st.title("Bot Question Test")

bot_id = st.text_input("Enter Bot ID:", "")  # Input for bot_id
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    selected_column = df.columns[0]  # Automatically select the first column
    
    if st.button("Activate"):
        # Combine all text in the selected column into one string
        combined_text = " ".join(df[selected_column].astype(str).tolist())
        
        with st.spinner("Processing your request..."):
        # Send the combined text to the API with the provided bot_id
            api_response = send_to_api(combined_text, bot_id)
            extracted_text = extract_text_from_json(api_response)
        
        # Display the extracted text
        #st.write(extracted_text)
        st.write("---")

        # Show download button only if extracted_text is available
        if extracted_text and extracted_text != "No output found in the response.":
            # Step 1: Save to a text file
            file_name = "response.txt"
            with open(file_name, "w") as f:
                f.write(extracted_text)
            
            # Step 2: Allow the user to download the file
            with open(file_name, "r") as f:
                st.download_button(
                    label="Download Response",
                    data=f,
                    file_name=file_name,
                    mime="text/plain"
                )
