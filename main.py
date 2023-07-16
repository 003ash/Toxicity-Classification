from flask import Flask, jsonify, request, render_template
import pickle
import pandas as pd
import scipy
import xgboost as xgb

import re
import string
import os
symbols = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')
def tokenize(s): return symbols.sub(r' \1 ', s).split()


hate_types = ['identity_hate', 'toxic', 'severe_toxic', 'obscene',
              'threat', 'insult']


loaded_models = []

for hate in hate_types:
    loaded_model = xgb.Booster()
    loaded_model.load_model(f"{hate}_xgboost.json")
    loaded_models.append(loaded_model)

def get_transformed(comments):
    comments_to_be_processed = pd.DataFrame(data={
        "comment_text": comments,
    })
    comments_to_be_processed_transformed = transform_function.transform(
        comments_to_be_processed['comment_text'])
    col = ['total_length', 'capitals', 'caps_vs_length', 'num_exclamation_marks', 'num_question_marks',
           'num_punctuation', 'num_symbols', 'num_words', 'num_unique_words', 'words_vs_unique', 'num_smilies']

    for data in [comments_to_be_processed]:
        data['total_length'] = data['comment_text'].apply(len)
        data['capitals'] = data['comment_text'].apply(
            lambda x: sum(1 for c in x if c.isupper()))
        data['caps_vs_length'] = data.apply(lambda row: float(row['capitals'])/float(row['total_length']),
                                            axis=1)
        data['num_exclamation_marks'] = data['comment_text'].apply(
            lambda x: x.count('!'))
        data['num_question_marks'] = data['comment_text'].apply(
            lambda x: x.count('?'))
        data['num_punctuation'] = data['comment_text'].apply(
            lambda x: sum(x.count(w) for w in '.,;:'))
        data['num_symbols'] = data['comment_text'].apply(
            lambda x: sum(x.count(w) for w in '*&$%'))
        data['num_words'] = data['comment_text'].apply(
            lambda x: len(x.split()))
        data['num_unique_words'] = data['comment_text'].apply(
            lambda x: len(set(w for w in x.split())))
        data['words_vs_unique'] = data['num_unique_words'] / data['num_words']
        data['num_smilies'] = data['comment_text'].apply(
            lambda x: sum(x.count(w) for w in (':-)', ':)', ';-)', ';)')))

    comments_to_be_processed_extract = scipy.sparse.csr_matrix(
        comments_to_be_processed[col].values)
    comments_to_be_processed_transformed = scipy.sparse.hstack(
        [comments_to_be_processed_extract, comments_to_be_processed_transformed])

    return comments_to_be_processed_transformed


def predict(comments):
    comments_transformed = get_transformed(comments)
    results = []
    response = []
    for model in loaded_models:
        results.append(model.predict(xgb.DMatrix(comments_transformed)))
    for index in range(len(comments)):
        res = {}
        for hateIndex in range(len(hate_types)):
            hate = hate_types[hateIndex]
            res[hate] = str(results[hateIndex][index])
        response.append({
            "comment": comments[index],
            "result": res
        })
    return response


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/doc/", methods=['GET'])
def doc():
    return render_template("doc.html")


@app.route("/", methods=['POST'])
def predict_hate():
    data = request.get_json()
    return jsonify(predict(data))


if __name__ == "__main__":
    app.run(debug=True)
