import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "0eb77a3d-81f6-4707-b80f-0b27282bac89"
FLOW_ID = "49de35fd-ba15-4259-9e8b-b856f3979dc4"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "results"

def run_flow(message: str) -> dict:
    """
    Call the Langflow API with the given message.
    
    Args:
        message (str): User input message
    
    Returns:
        dict: API response
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN, 
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
        return {"output": "Sorry, there was an error processing your request."}

def main():
    # Page configuration
    st.set_page_config(
        page_title="Medical Assistant Chatbot",
        page_icon="🩺",
        layout="centered"
    )

    # Custom CSS for improved styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .chat-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextArea textarea {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown("<h1 class='chat-header'>🩺 Medical Assistant Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("""<div class='chat-container'>
    This AI-powered medical assistant can help you with health-related queries. 
    Please note that this is an AI tool and should not replace professional medical advice.
    """, unsafe_allow_html=True)

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a medical question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = run_flow(prompt)
                bot_response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                st.markdown(bot_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    st.markdown("</div>", unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; color: #7f8c8d; font-size: 0.8em;'>
    🚨 Disclaimer: This chatbot provides general information and is not a substitute for 
    professional medical advice, diagnosis, or treatment.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()