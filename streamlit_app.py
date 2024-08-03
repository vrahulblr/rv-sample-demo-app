import streamlit as st
import json
import requests
import time
from newspaper import Article

# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

st.title("FastNews Article Summarizer")
st.markdown("**Generate summaries of online articles using abstractive summarization with Google's PEGASUS model.**")
st.subheader("Enter the URL of the article you want to summarize")
default_url = "https://"
url = st.text_input("URL:", default_url)

fetch_button = st.button("Fetch article")

API_KEY = st.text_input("Enter your HuggingFace API key", type="password")
submit_button = st.button("Submit")

headers_ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

if fetch_button:
    article_url = url
    session = requests.Session()

    try:
        response_ = session.get(article_url, headers=headers_, timeout=10)
    
        if response_.status_code == 200:

            with st.spinner('Fetching your article...'):
                time.sleep(3)
                st.success('Your article is ready for summarization!')

        else:
            st.write("Error occurred while fetching article.")

    except Exception as e:
        st.write(f"Error occurred while fetching article: {e}")

text = "Summarization failed"
if submit_button:
    article = Article(url)
    article.download()
    article.parse()
    title = article.title
    text = article.text

API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"

headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": text,
    "wait_for_model": True 
    })

# Display the results
summary = output[0]['summary_text'].replace('<n>', " ") 

st.divider()
st.subheader("Summary")
st.write(f"Your article: **{title}**")
st.write(f"**{summary}**")



