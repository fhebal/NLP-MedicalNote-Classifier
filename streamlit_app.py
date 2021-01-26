import streamlit as st
import yaml
from load_css import local_css
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import numpy as np
from random import sample
import os

local_css("style.css")

prediction_key = {
        0:'Gastroenterology',
        1:'Neurology',
        2:'Orthopedic',
        3:'Radiology',
        4:'Urology'
        }


class Highlighter():
    def __init__(self):
        self.start = "<span class='highlight blue'><span class='bold'>"
        self.end = "</span></span>"
    def highlight_match(self, text, config):
        for value in config:
            text = text.replace(" "+value+" ", "{0}"+value+"{1}")
        text = "<div>" + text.format(self.start, self.end) + "</div>"
        return text


# Load model from file
model = tf.keras.models.load_model('/home/muody/saved_model/my_model', compile=False)


# load data
def load_data():
    data_path = '/home/muody/data/medicalnotes/dataset/unlabeled-test-data/'
    files = os.listdir(data_path)
    sample_file = data_path + sample(files, 1)[0]
    with open(sample_file, 'r') as stream:
        sample_data = stream.read()
        sample_data = sample_data.replace('\n','')
        sample_data = sample_data.replace('</B>','')
        sample_data = sample_data.replace('<B>','')
    return sample_data


def main():
    # INPUT DATA
    #sample = st.text_input('Input your sentence here:')
    sample = load_data()
    prediction_arr = tf.sigmoid(model.predict(tf.convert_to_tensor([sample]))).numpy()
    prediction_num = np.argmax(prediction_arr)
    prediction = prediction_key[prediction_num]

    prediction_text = "<div>Prediction: <span class='highlight red'><span class='bold'>" + prediction + '</span></span></div>'

    st.markdown(prediction_text, unsafe_allow_html=True)
    st.write('\n')
    for key, value in prediction_key.items():
        st.write(value, prediction_arr[0][key])
    label = prediction_num
    with open("config/{}.yaml".format(label), 'r') as stream:
        try:
            config = stream.read().splitlines()
        except yaml.YAMLError as exc:
            print(exc)

    highlighter = Highlighter()
    t = highlighter.highlight_match(sample, config)
    st.markdown(t, unsafe_allow_html=True)


if st.button("New Text Sample"):
    main()
