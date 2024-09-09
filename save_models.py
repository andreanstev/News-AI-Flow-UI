from transformers import AutoModelForQuestionAnswering, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification
import os


save_directory = "./model"

# 1. Question Answering Model
qa_model_name = "Prasetyow12/bert-base-uncased-newsqa-squad-finetuned"
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_name)
qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_name)

qa_model_save_dir = os.path.join(save_directory, "question_answering")
os.makedirs(qa_model_save_dir, exist_ok=True)
qa_model.save_pretrained(qa_model_save_dir)
qa_tokenizer.save_pretrained(qa_model_save_dir)

print(f"Question Answering model saved in {qa_model_save_dir}")

# 2. Text Summarization Model
summ_model_name = "andreanstev/t5_small_news_summ"
summ_model = AutoModelForSeq2SeqLM.from_pretrained(summ_model_name)
summ_tokenizer = AutoTokenizer.from_pretrained(summ_model_name)

summ_model_save_dir = os.path.join(save_directory, "text_summarization")
os.makedirs(summ_model_save_dir, exist_ok=True)
summ_model.save_pretrained(summ_model_save_dir)
summ_tokenizer.save_pretrained(summ_model_save_dir)

print(f"Text Summarization model saved in {summ_model_save_dir}")

# 3. Text Classification Model
classifier_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
classifier_model = AutoModelForSequenceClassification.from_pretrained(classifier_model_name)
classifier_tokenizer = AutoTokenizer.from_pretrained(classifier_model_name)

classifier_model_save_dir = os.path.join(save_directory, "text_classification")
os.makedirs(classifier_model_save_dir, exist_ok=True)
classifier_model.save_pretrained(classifier_model_save_dir)
classifier_tokenizer.save_pretrained(classifier_model_save_dir)

print(f"Text Classification model saved in {classifier_model_save_dir}")