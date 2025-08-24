import streamlit as st
from datetime import datetime
from chatbot_backend import ask_bot

# --- Page Configuration and Custom CSS ---
# Using an absolute container for the chat input to keep it at the bottom.
# This avoids the need for a separate footer and keeps the layout tight.
st.set_page_config(
    page_title="AI Customer Service Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* General app background */
    .stApp {
        background-color: #0f1419;
        color: #ffffff;
    }
    
    /* Header styling */
    .chat-header {
        text-align: center;
        font-size: 1.5rem; /* Smaller font size */
        font-weight: 700;
        margin-bottom: 1rem; /* Smaller margin */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Message bubble styling */
    .user-message, .bot-message {
        padding: 0.75rem 1rem; /* Smaller padding */
        border-radius: 15px; /* Smaller rounded corners */
        font-size: 14px; /* Smaller font size */
        line-height: 1.4;
        margin: 0.25rem 0; /* Smaller margin between messages */
        max-width: 75%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        margin-left: auto;
        border-radius: 15px 15px 5px 15px;
        box-shadow: 0 2px 10px rgba(79, 172, 254, 0.2);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-right: auto;
        border-radius: 15px 15px 15px 5px;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.2);
    }
    
    .message-time {
        font-size: 0.65rem; /* Smaller time font */
        opacity: 0.6;
        margin-top: 0.25rem;
    }
    
    .user-time { text-align: right; }
    .bot-time { text-align: left; }
    
    /* Input and button styling */
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333; /* Thinner border */
        border-radius: 20px; /* Smaller rounded corners */
        padding: 10px 15px; /* Smaller padding */
        font-size: 14px; /* Smaller font size */
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 5px rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 40px; /* Smaller button */
        padding: 0.5rem 1.5rem; /* Smaller padding */
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .sidebar .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        width: 100%;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    
    .chat-stats {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.75rem; /* Smaller padding */
        border-radius: 8px; /* Smaller corners */
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 12px; /* Smaller font size */
    }
    
    .welcome-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem; /* Smaller padding */
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        font-size: 14px; /* Smaller font size */
    }

    /* New style for Quick Questions to make them smaller and inline */
    .quick-questions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-bottom: 10px;
    }

    .quick-questions-container .stButton > button {
        background: rgba(102, 126, 234, 0.1) !important;
        border: 1px solid #667eea !important;
        color: #667eea !important;
        border-radius: 15px !important;
        padding: 5px 10px !important; /* Even smaller padding for these buttons */
        font-size: 12px !important; /* Smaller font size */
        transition: all 0.3s ease !important;
        flex-grow: 1; /* Allow buttons to grow to fill space */
        min-width: fit-content;
    }

    .quick-questions-container .stButton > button:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State and UI Functions ---

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = """🎉 Welcome to AI Customer Service!

I'm your intelligent assistant, ready to help you with any questions or concerns. I have access to our comprehensive knowledge base and can provide detailed, accurate information.

Feel free to ask me anything! 💬"""
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome,
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    if "input_counter" not in st.session_state:
        st.session_state.input_counter = 0

def display_chat_messages():
    """Display all chat messages"""
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                💭 {message["content"]}
                <div class="message-time user-time">You • {message["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                🤖 {message["content"]}
                <div class="message-time bot-time">AI Assistant • {message["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("", unsafe_allow_html=True) # Small gap between messages

def handle_user_input():
    """Handle user input and generate bot response"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="💬 Type your question here...",
            key=f"user_input_{st.session_state.input_counter}",
            label_visibility="collapsed"
        )
    
    with col2:
        send_clicked = st.button("Send ➤", type="primary")
    
    if (send_clicked or user_input) and user_input.strip():
        process_message(user_input.strip())

def process_message(user_message):
    """Process user message and get bot response"""
    st.session_state.messages.append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    with st.spinner("🤖 AI is thinking..."):
        try:
            bot_response = ask_bot(user_message)
        except Exception as e:
            bot_response = f"❌ Sorry, I encountered an error: {str(e)}"
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    st.session_state.input_counter += 1
    st.rerun()

def create_sidebar():
    """Create sidebar with controls and quick actions"""
    with st.sidebar:
        st.markdown("## 🎛️ Chat Controls")
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.session_state.input_counter = 0
            welcome = """🎉 Welcome to AI Customer Service!
I'm your intelligent assistant, ready to help you with any questions or concerns. I have access to our comprehensive knowledge base and can provide detailed, accurate information.
Feel free to ask me anything! 💬"""
            st.session_state.messages.append({
                "role": "assistant",
                "content": welcome,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
        
        st.markdown("---")
        st.markdown("## ⚡ Quick Questions")
        
        quick_questions = [
            "What services do you provide?",
            "What are your pricing packages?",
            "What are your business hours?",
            "How can I contact support?",
            "What is your refund policy?"
        ]

        # Use columns to make buttons appear in a row
        cols = st.columns(2)
        
        for i, question in enumerate(quick_questions):
            with cols[i % 2]: # Distribute buttons into two columns
                if st.button(f"💡 {question}", key=f"quick_{i}"):
                    process_message(question)
        
        st.markdown("---")
        st.markdown("## 📊 Chat Statistics")
        st.markdown(f"""
        <div class="chat-stats">
            <strong>Total Messages:</strong> {len(st.session_state.messages)}<br>
            <strong>Your Questions:</strong> {len([m for m in st.session_state.messages if m['role'] == 'user'])}<br>
            <strong>AI Responses:</strong> {len([m for m in st.session_state.messages if m['role'] == 'assistant'])}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main app function"""
    initialize_session_state()
    
    st.markdown('<h1 class="chat-header">🤖 AI Customer Service Assistant</h1>', unsafe_allow_html=True)
    
    create_sidebar()
    
    # Main chat area with fixed height and a scrollbar
    chat_container = st.container()
    with chat_container:
        st.markdown("---")
        display_chat_messages()
    
    # Input field at the bottom of the page
    st.markdown("---")
    handle_user_input()

    # Footer
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 0.5rem;'>"
        "🤖 Powered by AI • Built with Streamlit • Always here to help!"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
