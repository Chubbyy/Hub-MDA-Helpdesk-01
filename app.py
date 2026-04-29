import os
import streamlit as st
import boto3
import datetime
import urllib.parse
import pandas as pd
from dotenv import load_dotenv
from PIL import Image

if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "last_tokens" not in st.session_state:
    st.session_state.last_tokens = 0

# Load information from .env file
load_dotenv()

# --- Configuration ---
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
ADMIN_PASS = os.getenv("ADMIN_PASS")
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0"

# Initialize the Bedrock Agent Runtime client
bedrock_client = boto3.client('bedrock-agent-runtime') #  region_name='us-east-1' if needed as second parameter

# --- Streamlit UI Configuration ---
favicon = Image.open("assets/MDA_favicon.png")

st.set_page_config(page_title="MDA Helpdesk AI", page_icon=favicon, layout="centered")

custom_css = """
            <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {display: none;}
            footer {visibility: hidden;}
            
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
    **:red[Phone: 666-666-6666]**\n
    **:red[Email: dummy_email@gmail.com]**
    """)

    st.divider()

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.session_id = None # Clears any memory of conversation being cleared
        st.rerun() # Refreshes the UI

    st.divider()

    with st.expander("Admin Panel"):
        if not st.session_state.admin_authenticated:
            with st.form("admin_login"):
                admin_pass = st.text_input("Enter Admin Key", type="password")
                submitted = st.form_submit_button("Authenticate")
                
            if submitted:
                if admin_pass == ADMIN_PASS:
                    st.session_state.admin_authenticated = True
                    st.rerun() # Instantly reloads to hide the login box
                else:
                    st.error("Incorrect Admin Key", icon="⚠️")
        
        else: # If they are already authenticated
            st.success("Authenticated", icon="✅")
            if st.button("Logout"):
                st.session_state.admin_authenticated = False
                st.rerun()
                
            try:
                df = pd.read_csv("audit_log.csv", names=["Timestamp", "Session ID", "User Query", "Status", "Mailto Triggered"])
                st.dataframe(df, width='stretch')
            except FileNotFoundError:
                st.warning("Audit log not found. No rejected inquiries have been generated yet.")
            except Exception as e:
                st.warning("An error occurred whilst trying to read the audit log.")

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
            request_params = {
                'input': {'text': prompt},
                'retrieveAndGenerateConfiguration': {
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                        'modelArn': MODEL_ARN,
                        'generationConfiguration': {
                            'promptTemplate': {
                                'textPromptTemplate': """You are a helpful, professional internal IT Helpdesk assistant for the Mississippi Development Authority (MDA). 

                                CRITICAL GUARDRAIL - HARDWARE BOUNDARY:
                                You are strictly prohibited from providing IT support for personal, home, or non-agency equipment. 
                                If the user's query explicitly mentions "home", "personal", "my own", or asks about physical devices not issued by MDA, you MUST refuse. Output EXACTLY this response: "I am authorized to assist with MDA-issued hardware and enterprise systems only. For security reasons, I cannot provide troubleshooting steps for personal or home devices. If you need further assistance, please contact the human IT Helpdesk directly at 666-666-6666 or dummy_email@gmail.com."

                                GENERAL INSTRUCTIONS & CONVERSATION HANDLING:
                                1. Answer the user's question using the provided search results and previous conversational context. Do NOT include your internal reasoning, plans, or thinking processes.
                                2. Output ONLY the final answer directly to the user in a friendly tone. Format your response cleanly using bullet points or numbered lists where appropriate.
                                3. CONTEXTUAL AWARENESS & VALIDATION: Always evaluate the user's query against the recent conversation history first. If the user asks a follow-up question or provides a value to check (e.g., "Is this valid?", "What about X?"), you MUST use the rules, definitions, or steps provided in your immediately preceding answers to evaluate it. Do not treat follow-ups as isolated requests. CRITICAL: When validating any value or scenario against a set of rules, you MUST perform a strict, step-by-step evaluation against EVERY applicable rule one by one before providing your final conclusion.
                                4. ESCALATION PROTOCOL: If the provided search results and conversation history do not contain the answer to a query (e.g., PTO requests, HR policies), do NOT guess or make up information. You MUST output EXACTLY this response: "I cannot find information regarding this request in the IT documentation. Please contact the human IT Helpdesk directly at 666-666-6666 or dummy_email@gmail.com for further assistance."

                                SOCIAL GRACE EXCEPTION:
                                If the user's input is a simple greeting, expression of gratitude ("thank you", "it works"), or sign-off, you may respond naturally and politely without needing search results. Do NOT trigger the escalation protocol for these social pleasantries.

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
            }

            if st.session_state.session_id:
                request_params['sessionId'] = st.session_state.session_id
            
            response = bedrock_client.retrieve_and_generate(**request_params)

            st.session_state.session_id = response.get('sessionId')
            
            bot_response = response['output']['text']

            mailto_triggered = "No"
            if "dummy_email@gmail.com" in bot_response or "deskinfo@mississippi.org" in bot_response:
                mailto_triggered = "Yes"
                
                # Grabs up to the last 5 messages (to stay under the 2000-char mailto: limit)
                recent_history = st.session_state.messages[-5:]
                
                # Format the history into a readable text block
                history_text = "--- RECENT CHAT CONTEXT ---\n"
                for msg in recent_history:
                    role = "User" if msg["role"] == "user" else "AI Assistant"
                    history_text += f"{role}: {msg['content']}\n\n"
                history_text += "---------------------------\n\n"
                
                # URL-encode the entire block (including spaces, newlines, and special characters)
                encoded_body = urllib.parse.quote(f"Automated Ticket Draft:\n\nPlease assist with the following issue. The user's recent interaction with the AI Assistant is included below for context.\n\n{history_text}")
                
                email_link = f"mailto:dummy_email@gmail.com?subject=IT%20Helpdesk%20Escalation&body={encoded_body}"
                bot_response += f"\n\n**[📥 Click here to automatically draft an email to the Helpdesk]({email_link})**"

            if "I am authorized to assist with MDA-issued" in bot_response or mailto_triggered == "Yes":
                # Determine the type of log entry
                status = "GUARDRAIL BLOCK" if "I am authorized to assist" in bot_response else "ESCALATED"
                
                with open("audit_log.csv", "a") as log_file:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f'"{timestamp}","{st.session_state.session_id}","{prompt}","{status}","{mailto_triggered}"\n')
            
        except Exception as e:
            bot_response = f"Error connecting to AWS: {str(e)}"
        
        st.session_state.last_tokens = (len(prompt) // 4) + (len(bot_response) // 4)

    with st.chat_message("assistant", avatar="assets/AvatarIcon.png"):
        st.markdown(bot_response)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Calculate and display token count in the sidebar
if st.session_state.last_tokens > 0:
    st.sidebar.caption(f"⚡ **Last Query:** ~{st.session_state.last_tokens} tokens utilized")
