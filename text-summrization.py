import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

nlp = spacy.load('en_core_web_sm')


st.set_page_config(page_title="Text Summarizer", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
        color: #333;
    }
        .stTextArea>textarea {
        border: 3px solid;
        border-image-source: linear-gradient(to right, #ff7e5f, #feb47b);
        border-image-slice: 1;
        border-radius: 10px;
        padding: 20px;
        font-size: 90px;  # Updated font size
        height: 300px;
        overflow-y: auto;
        }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stTextArea>textarea {
        border: 3px solid;
        border-image-source: linear-gradient(to right, #ff7e5f, #feb47b);
        border-image-slice: 1;
        border-radius: 10px;
        padding: 20px;
        font-size: 18px;
        height: 300px;
        overflow-y: auto;
    }
    .stMarkdown {
        font-size: 20px;
        line-height: 1.8;
        text-align: center;
    }
    .summary-box {
        background-color:#525252  ;
        color: white;
        padding: 20px;
        border-image-slice: 1;
        margin: 15px auto;
        max-width: 1000px;
    }
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .animated-header {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(45deg, #ff7e5f, #feb47b, #4CAF50);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientAnimation 3s ease infinite;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """<h1 class="animated-header">Text Summarization</h1>""",
    unsafe_allow_html=True
)
st.markdown(
    """<p style="font-size:22px; text-align:center;">This app summarizes a given text using Natural Language Processing (NLP). Enter text below to get started.</p>""",
    unsafe_allow_html=True
)

text = st.text_area("Enter the text you want to summarize:", placeholder="Paste your text here...")

if st.button("Summarize"):
    if text.strip():
        stopwords = list(STOP_WORDS)
        doc = nlp(text)

        word_freq = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1 

        max_freq = max(word_freq.values())
        for word in word_freq.keys():
            word_freq[word] = word_freq[word] / max_freq

        sent_tokens = [sent for sent in doc.sents]
        sent_scores = {}
        for sent in sent_tokens:
            for word in sent:
                if word.text in word_freq.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word.text]
                    else:
                        sent_scores[sent] += word_freq[word.text]

        
        select_len = int(len(sent_tokens) * 0.5)
        summary = nlargest(select_len, sent_scores, key=sent_scores.get)
        final_summary = ' '.join([sent.text for sent in summary])

       
        st.subheader("Original Text")
        st.markdown(f"<div class='summary-box'>{text}</div>", unsafe_allow_html=True)

        st.subheader("Summary")
        st.markdown(f"<div class='summary-box'>{final_summary}</div>", unsafe_allow_html=True)

        st.subheader("Statistics")
        st.markdown(
            f"""<ul style="text-align:center; list-style:none;">
            <li><strong>Original Text Length:</strong> {len(text.split())} words</li>
            <li><strong>Summary Length:</strong> {len(final_summary.split())} words</li>
            <li><strong>Compression Ratio:</strong> {len(final_summary.split()) / len(text.split()):.2f}</li>
            </ul>""",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter some text to summarize.")

st.markdown("---")