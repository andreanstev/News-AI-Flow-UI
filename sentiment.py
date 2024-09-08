import streamlit as st
from models import get_news_from_url, news_info_template, sentiment


def get_model_desc(model_name):
    if model_name=="Sentiment-1":
        desc = "Precision: 0.92; Recall: 0.91"
    elif model_name=="Sentiment-2":
        desc = "Precision: 0.89; Recall: 0.92"
    elif model_name=="Sentiment-3":
        desc = "Precision: 0.93; Recall: 0.95"
    else:
        desc = "no selected model"     
    return desc

# session
if "news" not in st.session_state:
    st.session_state["news"] = ""
if "sentiment" not in st.session_state:
    st.session_state["sentiment"] = {"result":"","score":0.00}


st.title("😐 Sentiment Analysis")

option = st.selectbox("Select your model",
                    ("-","Sentiment-1", "Sentiment-2", "Sentiment-3"),)

desc = get_model_desc(option)
if option!='-':
    st.write("🎯 Model performance (evaluation):", desc)
    
    txt_input = st.text_area('**Enter News Text/URL**', '', height=90)
    submit = st.button("Submit")
    
    if submit:
        news = get_news_from_url(txt_input)
        st.session_state["news"] = news["text"]
        sentiment_result = sentiment(st.session_state["news"] )
        st.session_state["sentiment"]["result"] = sentiment_result["sentiment"]
        st.session_state["sentiment"]["score"] = sentiment_result["score"]
        
        for k,v in st.session_state.items():
            if k=='news':
                txt_input = st.text_area('**News Info**', st.session_state["news"], height=60, disabled=True)
            if k=="sentiment" and st.session_state["sentiment"]["result"]!='':
                sentiment_ = st.session_state["sentiment"]["result"]
                score_ = st.session_state["sentiment"]["score"]
                result = f"{sentiment_} ({score_})"
                st.write("**Sentiment**")
                st.info(result)
else:
    st.write("No model selected")





    