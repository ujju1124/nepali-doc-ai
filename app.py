"""
Nepal Doc AI - Nepali Document Intelligence App
Streamlit interface for OCR extraction and intelligent document Q&A
"""

import streamlit as st
from dotenv import load_dotenv
import os
from ocr import extract_text_from_document
from intelligence import generate_summary, answer_question

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Nepal Doc AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        color: #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'ocr_result' not in st.session_state:
    st.session_state.ocr_result = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Main header
st.markdown("<h1 class='main-header'>📄 Nepal Doc AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Upload any Nepali document and get instant summaries and answers</p>", unsafe_allow_html=True)

# File uploader
st.markdown("---")
uploaded_file = st.file_uploader(
    "Upload Document (JPG, PNG, or PDF)",
    type=['jpg', 'jpeg', 'png', 'pdf'],
    help="Upload a clear photo of your Nepali document"
)

if uploaded_file is not None:
    # Display uploaded image/document info
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Uploaded Document")
        if uploaded_file.type == "application/pdf":
            st.info("📑 PDF uploaded - first page will be processed")
        else:
            st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
    
    with col2:
        st.subheader("📊 Document Info")
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
        st.write(f"**Type:** {uploaded_file.type}")
    
    # Process document button
    if st.button("🔍 Extract & Analyze Document", type="primary"):
        # Reset previous results
        st.session_state.extracted_text = None
        st.session_state.ocr_result = None
        st.session_state.summary = None
        st.session_state.chat_history = []
        
        # Read file bytes
        file_bytes = uploaded_file.read()
        
        # Step 1: OCR Extraction
        with st.spinner("🔄 Extracting text from document... This may take 10-30 seconds..."):
            ocr_result = extract_text_from_document(file_bytes, uploaded_file.name)
            st.session_state.ocr_result = ocr_result
        
        if not ocr_result['success']:
            st.error(f"❌ {ocr_result['error']}")
        elif ocr_result['word_count'] == 0:
            st.error("❌ No text detected in the document. Please upload a clearer image.")
        else:
            st.session_state.extracted_text = ocr_result['cleaned_text']
            
            # Display OCR metrics
            st.success(f"✅ Text extracted successfully!")
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Words Extracted", ocr_result['word_count'])
            with metric_col2:
                st.metric("OCR Confidence", f"{ocr_result['confidence_score']:.1f}%")
            
            # Warning for low confidence
            if ocr_result['confidence_score'] < 50:
                st.markdown(
                    "<div class='warning-box'>"
                    "⚠️ <b>Low confidence</b> — Image quality may affect accuracy. "
                    "Consider uploading a clearer image for better results."
                    "</div>",
                    unsafe_allow_html=True
                )
            
            # Step 2: Generate Summary
            with st.spinner("🤖 Analyzing document and generating summaries..."):
                summary_result = generate_summary(ocr_result['cleaned_text'])
                st.session_state.summary = summary_result
            
            if not summary_result['success']:
                st.error(f"❌ {summary_result['error']}")

# Display results if available
if st.session_state.extracted_text:
    st.markdown("---")
    
    # Extracted text in expandable section
    with st.expander("📝 View Extracted Text", expanded=False):
        st.text_area(
            "Extracted Text",
            st.session_state.extracted_text,
            height=200,
            disabled=True
        )
    
    # Display summaries if available
    if st.session_state.summary and st.session_state.summary['success']:
        st.markdown("---")
        st.subheader("📋 Document Summaries")
        
        sum_col1, sum_col2 = st.columns(2)
        
        with sum_col1:
            st.markdown("**🇬🇧 English Summary**")
            st.info(st.session_state.summary['english_summary'])
        
        with sum_col2:
            st.markdown("**🇳🇵 Nepali Summary**")
            st.info(st.session_state.summary['nepali_summary'])
        
        # Key facts
        st.markdown("**🔑 Key Facts**")
        for i, fact in enumerate(st.session_state.summary['key_facts'], 1):
            st.markdown(f"{i}. {fact}")
        
        # Chat interface
        st.markdown("---")
        st.subheader("💬 Ask Questions About This Document")
        st.caption("Ask anything about the document in English or Nepali")
        
        # Display chat history
        for question, answer in st.session_state.chat_history:
            st.markdown(f"<div class='chat-message user-message'><b>You:</b> {question}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-message assistant-message'><b>AI:</b> {answer}</div>", unsafe_allow_html=True)
        
        # Question input
        question = st.text_input("Your question:", key="question_input", placeholder="e.g., What is the document date? / यो कागजात कहिलेको हो?")
        
        if st.button("Send Question", type="secondary"):
            if question.strip():
                with st.spinner("🤔 Thinking..."):
                    answer_result = answer_question(
                        st.session_state.extracted_text,
                        question,
                        st.session_state.chat_history
                    )
                
                if answer_result['success']:
                    # Add to chat history
                    st.session_state.chat_history.append((question, answer_result['answer']))
                    st.rerun()
                else:
                    st.error(f"❌ {answer_result['error']}")
            else:
                st.warning("⚠️ Please enter a question")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "Nepal Doc AI • Powered by EasyOCR & Groq • Built with Streamlit"
    "</p>",
    unsafe_allow_html=True
)
