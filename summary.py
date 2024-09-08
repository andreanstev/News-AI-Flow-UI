import streamlit as st
from models import summarizer, get_news_from_url

# session
if "news" not in st.session_state:
    st.session_state["news"] = ""
if "summary" not in st.session_state:
    st.session_state["summary"] = ""


st.title("🗒️ Text Summarization")

txt_input = st.text_area('**Enter News Text/URL**', '', height=90)
submit = st.button("Submit")

if submit:
    news = get_news_from_url(txt_input)
    st.session_state["news"] = news["text"]
    summary = summarizer(st.session_state["news"] )
    st.session_state["summary"] = summary
    
    for k,v in st.session_state.items():
        if k=='news':
            txt_input = st.text_area('**News Info**', st.session_state["news"], height=60, disabled=True)
        if k=="summary" and st.session_state["summary"]!='':
            st.write("**Summary**")
            st.info(st.session_state["summary"])