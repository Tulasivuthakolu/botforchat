import openai
import streamlit as st

# Get API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# Title and caption
st.title("😎 Chatbot")
st.caption("🤗 A Streamlit chatbot created by Tulasi Vuthakolu")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input field for user prompt
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    # Initialize OpenAI client
    openai.api_key = openai_api_key
    
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Get response from OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message["content"]
    except Exception as e:
        msg = "Sorry, something went wrong. Please try again later."
    
    # Append assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
