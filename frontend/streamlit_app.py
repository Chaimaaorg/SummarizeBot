import streamlit as st
from util_functions import clean_summary, get_summary, load_css

st.set_page_config(
    page_title="Text Summarizer",
    page_icon="📝",
    layout="wide"
)

load_css()


st.markdown("<h1 class='big-font'>Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown("### Enter the text you want to summarize")

# Text area with spellcheck disabled
text_to_summarize = st.text_area(
    "",
    height=300,
    placeholder="Paste your text here...",
    label_visibility="collapsed",
)

if st.button("Summarize", key="summarize-button-action"):
    if text_to_summarize:
        with st.spinner("Generating summary..."):
            summary_result = get_summary(text_to_summarize)
            
            if "error" in summary_result:
                st.error(summary_result)
            else:
                cleaned_summary = clean_summary(summary_result)
                st.markdown("### Summary")
                st.markdown(f"""
                    <div class='summary-box'>
                        <p>{cleaned_summary}</p>
                    </div>
                """, unsafe_allow_html=True)

                summary_text = str(cleaned_summary)
                st.download_button(
                    label="Download Summary",
                    data=summary_text,
                    file_name="summary.txt",
                    mime="text/plain"
                )
    else:
        st.warning("Please enter some text to summarize.")

st.sidebar.markdown("### About Text Summarization")
st.sidebar.info(
    "Our text summarization tool uses advanced AI to condense large texts "
    "while preserving key information. Perfect for quickly understanding "
    "articles, reports, and documents."
)
