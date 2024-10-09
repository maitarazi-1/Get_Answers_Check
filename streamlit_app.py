import streamlit as st
import requests
import json

def send_to_api(text):
    url = "https://langflow-fe-jeen.delightfulwater-ecb5056f.westeurope.azurecontainerapps.io/api/v1/run/38119a37-38a5-4566-810c-4ac486f0c7be?stream=false"
    payload = {
        "input_value": text,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "CustomComponent-Mc9Bb": {},
            "ParseData-FiFMM": {},
            "ParseData-PciqQ": {},
            "JeenAssistantTriggerComponentChainRequests-RyHsl": {},
            "ChatOutput-rJKBM": {},
            "ChatInput-wWLuP": {},
            "CustomComponent-BJz55": {},
            "ParseData-lwUUv": {}
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
        print("Raw JSON data:", json_data)
        text = json_data['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        print("Extracted text before parsing:", text)
        try:
            text_data = json.loads(text)
            return text_data['value']
        except json.JSONDecodeError as json_error:
            print(f"JSON parsing error: {str(json_error)}")
            return text
    except KeyError as key_error:
        return f"Error extracting text: KeyError - {str(key_error)}"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

st.title("Text to API Processor")

user_input = st.text_area("Enter your text here:")

if st.button("Send to API"):
    if user_input.strip():
        st.write("Sending text to API...")
        api_response = send_to_api(user_input)
        extracted_text = extract_text_from_json(api_response)
        st.write("API Response:")
        st.write(extracted_text)
    else:
        st.warning("Please enter some text before sending.")

st.write("Type your message, click the button, and see the API's response below.")
