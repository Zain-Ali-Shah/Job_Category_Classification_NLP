from flask import Flask,request,jsonify,render_template
import joblib
import re
import spacy
import json
from flask_cors import CORS

#   CREATE FLASK APP
app=Flask(__name__)
cors = CORS(app)

# load english language model and create nlp object from it
nlp = spacy.load("en_core_web_sm")

category_mapping={
    0:'Engineering',
    1:'Healthcare Nursing',
    2:'Accounting Finance',
    3:'Sales'
}

def preprocess(text):
    # clean the text
    clean_text = re.sub('http\S+\s*', ' ', text)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('#\S+', '', clean_text)
    clean_text = re.sub('@\S+', '  ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    # remove stop words and lemmatize the text
    doc = nlp(clean_text)
    filtered_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        filtered_tokens.append(token.lemma_)
    return " ".join(filtered_tokens)

def preprocess_title(text):
    # remove stop words and lemmatize the text
    doc = nlp(text)
    filtered_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        filtered_tokens.append(token.lemma_.lower())

    return " ".join(filtered_tokens)

loaded_model = joblib.load('SVC_tfidf_model.joblib')

#   CONNECT POST API CALL --> predict() Function
#   http://localhost:5000/predict
@app.route('/predict-category',methods=['POST'])
def predict():
    description=request.json
    preprocess_description=preprocess(description['description'])
    print(preprocess_description)
    predicted_category=loaded_model.predict([preprocess_description])
    category_name=category_mapping.get(predicted_category[0],'Unknown')
    return jsonify({'prediction':category_name})

if __name__=='__main__':
    app.run(debug=True)