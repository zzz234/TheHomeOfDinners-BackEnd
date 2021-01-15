import json
import os
import time
from threading import Thread
import requests

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from google_trans_new import google_translator

vocabulary = None
transformer = None
svm = None

initialing = False
translator = google_translator()


def do_initial():
    global vocabulary, transformer, svm, initialing
    initialing = True
    base_url = os.path.abspath('TheHomeOfDinners\\AIModule\\models')
    if not vocabulary:
        vocabulary = joblib.load(os.path.join(base_url, 'vocabulary.m'))  # 加载词库
        print('load vocabulary successful!')
    if not transformer:
        transformer = joblib.load(os.path.join(base_url, 'transformer.m'))  # 加载transform模型
        print('load transformer successful!')
    if not svm:
        svm = joblib.load(os.path.join(base_url, 'svm_wordbag_train_model.m'))  # 加载预测的模型
        print('load model successful!')
    initialing = False


def initial():
    Thread(target=do_initial).start()


def analyze(text):
    """
    :param text:输入的文本，需以列表形式存在
    :return:预测值：1表示neg，0表示pos
    """
    assert isinstance(text, str)
    if not (vocabulary and svm and transformer):
        if not initialing:
            initial()
        print("initialing...")
        time.sleep(1)
    # 翻译
    text = [translator.translate(text, lang_tgt='en')]
    # assert isinstance(text, list)

    vectorizer = CountVectorizer(
        decode_error='ignore',
        strip_accents='ascii',
        vocabulary=vocabulary,
        stop_words='english',
        max_df=1.0, binary=True,
        min_df=1)
    text = vectorizer.fit_transform(text)
    text = text.toarray()

    text = transformer.transform(text)
    text = text.toarray()

    y_pred = svm.predict(text)
    return y_pred
