import re
import streamlit as st
from newspaper import Article

### SESSION ###
def clear_session():
    if len(list(st.session_state.keys()))>0:
        for key in st.session_state.keys():
            del st.session_state[key]
    print("Session cleared!")
    return True

### NEWS SCRAPER ###
def is_url(input_text):
    # Regular expression for detecting a valid URL
    url_regex = re.compile(
        r'^(https?:\/\/)?'  # Optional http or https scheme
        r'([\da-z\.-]+)\.'  # Domain name and extension
        r'([a-z\.]{2,6})'   # Top-level domain (TLD)
        # r'([\/\w \.-]*)*\/?$'  # Path
    )
    return re.match(url_regex, input_text) is not None

def cleaning_multiline(input_text):
    multiline_regex = r'\n+'
    return re.sub(multiline_regex,"\n",input_text)
    

def get_news_from_url(input_text):
    is_url_check = is_url(input_text)
    
    if is_url_check: # input is URL
        print("Input text is an URL")
        try:
            article = Article(input_text)
            article.download()
            article.parse()
            title = article.title
            text = article.text
            pub_date = article.publish_date
            return {
                "title":title,
                "text":text,
                "pub_date":pub_date,
            }
        except Exception as E:
            print("Exception:",E)
            return {
                "title":'-',
                "text":'-',
                "pub_date":'-',
            } 
    else: # input is non URL
        print("Input text is not an URL")
        return {
            "title":'-',
            "text":input_text,
            "pub_date":'-',
        }

news_info_template = """
{title} \n
{pub_date} \n
{text}
""".strip()


### QA ###
def prepare_qa(input_text,user_question):
    # commands here
    return input_text

### SENTIMENT ###
def sentiment(input_text):
    # commands here
    return {"sentiment":"Positive","score":0.89}

### SUMMARIZATION ###
def summarizer(input_text):
    # commands here
    print("length input",len(input_text))
    length = int(round(len(input_text)*0.5))
    print("length",length)
    return input_text[:length]

def translate_en2id(input_text):
    # commands here
    return input_text