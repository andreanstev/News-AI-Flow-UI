import re
import streamlit as st
from newspaper import Article
from transformers import pipeline
import torch
import pandas as pd
import logging
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt_tab')
nltk.download('punkt')



if torch.cuda.is_available():
    device = 'cuda'
    logging.info("GPU enabled")
else:
    device = 'cpu'
    logging.info("GPU disabled, use CPU instead")

### SESSION ###
def clear_session():
    if len(list(st.session_state.keys()))>0:
        for key in st.session_state.keys():
            del st.session_state[key]
    logging.info("Session cleared!")
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
        logging.info("Input text is an URL")
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
            logging.info("Exception: "+str(E))
            return {
                "title":'-',
                "text":'-',
                "pub_date":'-',
            } 
    else: # input is non URL
        logging.info("Input text is not an URL")
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


def clean_text(text):
    # Definisikan pola regex untuk berbagai pembersihan
    url_pattern = re.compile(r'https?://\S+|www\.\S+', re.IGNORECASE)
    hashtag_pattern = re.compile(r'#\w+', re.IGNORECASE)
    double_space_pattern = re.compile(r'\s\s+')
    header_pattern = re.compile(r'^.*?--\s?', re.IGNORECASE)
    video_pattern = re.compile(r'VIDEO:.*?(?:\.\s|$)', re.IGNORECASE)

    # Hapus URL
    text = url_pattern.sub('', text)

    # Hapus hashtag
    text = hashtag_pattern.sub('', text)

    # Cek jika ada '--' dalam 40 karakter pertama
    if '--' in text[:40]:
        # Hapus header sebelum '--'
        text = header_pattern.sub('', text).strip()

    # Hapus frasa "VIDEO:" hingga titik
    text = video_pattern.sub('', text)

    # Hapus double space
    text = double_space_pattern.sub(' ', text)

    # Trim leading and trailing spaces
    text = text.strip()

    return text

### QA ###
def prepare_qa(input_text,user_question):
    qa = pipeline("question-answering", model="./model/question_answering", device = device)
    res = qa(question=user_question, context=clean_text(input_text))
    logging.info(str(res['answer']))
    return res['answer']

### SENTIMENT ###
def sentiment(input_text):
    classifier = pipeline("text-classification", model="./model/text_classification", device = device)
    def split_into_sentences(text):
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        return sentences
    logging.info(input_text)
    splitted_text = split_into_sentences(input_text)
    if len(splitted_text)>1:
        avg_len = sum([len(i) for i in splitted_text])/len(splitted_text)
        splitted_text_filtered = [i for i in splitted_text if len(i)>=int(avg_len)]

        res = classifier(splitted_text_filtered)
        df = pd.DataFrame(res)
        sentiment = df['label'].value_counts().index[0] # ambil sentimen yang dominan
        score = df.groupby('label').mean().loc[sentiment]['score'] # rata2 skor dari sentiment dominan

    else:
        res = classifier(input_text)
        sentiment = res[0]['label']
        score = res[0]['score']
    return {'sentiment': sentiment, 'score': score}

### SUMMARIZATION ###
def summarizer(input_text, out_max_length=516):
    summ = pipeline("text2text-generation", model="./model/text_summarization", max_length=out_max_length, device = device)
    res = summ(clean_text(input_text))
    res = res[0]['generated_text']
    logging.info("length input "+str(len(input_text)))
    # length = int(round(len(input_text)*0.5))
    logging.info("length summarized "+str(len(res)))
    return res

def translate_en2id(input_text):
    # commands here
    return input_text