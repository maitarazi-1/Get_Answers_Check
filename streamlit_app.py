import streamlit as st
import pandas as pd
import requests
import json

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
    st.write("Raw JSON response:", json_data)
    try:
        # Adjust the path to match the API's actual JSON structure
        text = json_data.get('message', {}).get('data', {}).get('text', 'Text not found')
        return text
    except KeyError as key_error:
        return f"Error extracting text: KeyError - {str(key_error)}"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

st.title("Bot Question Test")

bot_id = st.text_input("Enter Bot ID:", "")  # Input for bot_id
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    selected_column = df.columns[0]  # Automatically select the first column
    #st.write("Automatically selected column:", selected_column)
    
    if st.button("Activate"):
        #st.write(f"Processing column: {selected_column}")
        
        # Combine all text in the selected column into one string
        combined_text = " ".join(df[selected_column].astype(str).tolist())
        
        #st.write("Combined Text:", combined_text)
        
        # Send the combined text to the API with the provided bot_id
        api_response = send_to_api(combined_text, bot_id)
        extracted_text = extract_text_from_json(api_response)
        
        st.write("API Response:")
        st.write(extracted_text)
        st.write("---")