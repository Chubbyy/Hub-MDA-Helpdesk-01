import os
import streamlit as st
import boto3
from dotenv import load_dotenv
from PIL import Image

# Load information from .env file
load_dotenv()

# --- Configuration ---
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0"

# Initialize the Bedrock Agent Runtime client
bedrock_client = boto3.client('bedrock-agent-runtime') #  region_name='us-east-1' if needed as second param

# --- Streamlit UI Configuration ---
favicon = Image.open("assets/MDA_favicon.png")

st.set_page_config(page_title="MDA Helpdesk AI", page_icon=favicon, layout="centered")

custom_css = """
            <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {display: none;}
            footer {visibility: hidden;}
            
            /* Override Streamlit's default rounded corners on images */
            [data-testid="stImage"] img {
                border-radius: 0px !important;
            }
            </style>
            """
st.html(custom_css)

st.image("assets/MS MDA logo.png", width=250)

st.title("MDA IT Helpdesk Assistant")
st.markdown("**:red[Ask me questions about ACE, MAGIC, passwords, hardware, and network access.]**")

st.divider()

with st.sidebar:
    st.image("assets/MS MDA logo.png", width=200)
    st.markdown("### IT Helpdesk Hub")
    st.markdown("Designed to assist MDA employees in quickly resolving IT issues and answering general, relevant inquiries.")
    
    st.divider()

    st.markdown("""
    **:red[CONTACT:]**\n
    **:red[Phone: 666-6666]**\n
    **:red[Email: dummy_email@gmail.com]**
    """)

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun() # Refreshes the UI

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages on app rerun
for message in st.session_state.messages:
    # Set the avatar based on who is talking
    avatar_img = "assets/AvatarIcon.png" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_img):
        st.markdown(message["content"])

# --- Chat Interaction ---
if prompt := st.chat_input("E.g., How do I reset my password?"):
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        try:
            response = bedrock_client.retrieve_and_generate(
                input={
                    'text': prompt
                },
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                        'modelArn': MODEL_ARN,
                        'generationConfiguration': {
                            'promptTemplate': {
                                'textPromptTemplate': """You are a helpful, professional internal IT Helpdesk assistant for the Mississippi Development Authority (MDA). 
                                Answer the user's question using ONLY the provided search results. Do NOT include your internal reasoning, plans, or thinking processes. Output ONLY the final answer directly to the user in a friendly tone. Format your response cleanly using bullet points or numbered lists where appropriate.
                                
                                If the provided search results do not contain the answer, do NOT guess or make up information. Instead, politely apologize and instruct the user to contact the human IT Helpdesk directly at 666-666-6666 or dummy_email@gmail.com.

                                Search results: $search_results$
                                
                                User query: $query$"""
                            },
                            'inferenceConfig': {
                                'textInferenceConfig': {
                                    'maxTokens': 1000,
                                    'temperature': 0.1
                                }
                            }
                        }
                    }
                }
            )
            
            bot_response = response['output']['text']

            if "dummy_email@gmail.com" in bot_response:
                encoded_prompt = prompt.replace(" ", "%20")
                email_link = f"mailto:dummy_email@gmail.com?subject=IT%20Helpdesk%20Escalation&body=Automated%20Ticket%20Draft:%0A%0AUser%20Inquiry:%20{encoded_prompt}%0A%0APlease%20assist%20with%20this%20issue."
                
                bot_response += f"\n\n**[📥 Click here to automatically draft an email to the Helpdesk]({email_link})**"
            
        except Exception as e:
            bot_response = f"Error connecting to AWS: {str(e)}"

    with st.chat_message("assistant", avatar="assets/AvatarIcon.png"):
        st.markdown(bot_response)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_response})