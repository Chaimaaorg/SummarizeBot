import streamlit as st
import requests
import re
from styles import CSS 

def load_css():
    st.markdown(CSS, unsafe_allow_html=True)
    
def get_summary(text):
    try:
        api_url = "http://fastapi_server:9090/api/v1/get_summary"  # Update to correct API URL
        
        payload = {
            "text": text
        }
        
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return {"error": f"Failed to get summary: {response.text}"}
    
    except Exception as e:
        st.error(f"Error calling summarize API: {str(e)}")
        return {"error": f"Failed to get summary: {str(e)}"}


def clean_summary(summary):
    # Regex to remove 'summarizer_tool:' and everything before it
    cleaned_summary = re.sub(r"^summarizer_tool:\s*", "", summary)
    return cleaned_summary