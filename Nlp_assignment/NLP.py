import nltk
import PyPDF2
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import openai



# extract the text from pdf
def extrct_text(path):
    # creating a pdf file object
    pdfFileObj = open(path, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # string file for storing extracted text
    text_1 = ''

    #choose the page size correctly as gpt model only allows 4098 token at a time
    for i in range(1,6):
        # creating a page object
        pageObj = pdfReader.pages[i]

        # extracting text from page
        text_1 += pageObj.extract_text()
    return text_1

path=r"C:\Users\Barry\Desktop\projects\akaike assignment\NLP task\chapter-3.pdf" #provide file path
text_1 = extrct_text(path)


def pre_processing(text_1):
    # convert the paragraph into sentence using nltk(sent_tokenizer) package
    sentences = nltk.sent_tokenize(text_1)

    # Remove stopwords, punctuation and digits from the text
    # Remove everything other than letters
    clean_text = re.sub('[^a-zA-Z]+', ' ', str(sentences))

    # Replace multiple spaces with a single space
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text
clean_text= pre_processing(text_1)



#generate your OPNE API KEY and paste within the quotes
openai.api_key  = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

text = f"""
{clean_text}

"""
prompt = f"""
read and understand  the text delimited by triple backticks \ 
and form the MCQ's in such way that it seems to have two correct answers to confuse students,\
like shown below

1. question?
A) option 1
B) option 2
C) option 3
D) option 4
Correct options: 1 and 3

```{text}```
"""
response = get_completion(prompt)
print(response)