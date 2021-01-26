import streamlit as st
import yaml
from load_css import local_css
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import numpy as np

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
            text = text.replace(value, "{0}"+value+"{1}")
        text = "<div>" + text.format(self.start, self.end) + "</div>"
        return text


# Load model from file
model = tf.keras.models.load_model('/home/muody/saved_model/my_model', compile=False)
#load data
medical_notes_dir = '/home/muody/data/medicalnotes/dataset/train-data'
sample_data = tf.keras.preprocessing.text_dataset_from_directory(
    medical_notes_dir,
    batch_size=32)

def main():
    # INPUT DATA
    #sentence = st.text_input('Input your sentence here:')
    #st.write(model.predict(sentence))
    sample = [x.numpy()[0] for x, y in sample_data.take(1)][0].decode('utf-8')
    sample = sample.replace('\n','').replace('<B>','').replace('</B>','')
    prediction_num = np.argmax(model.predict([sample]))
    prediction = prediction_key[prediction_num]

    st.write(prediction, prediction_num)
    label = prediction_num
    with open("config/{}.yaml".format(label), 'r') as stream:
        try:
            config = stream.read().splitlines()
        except yaml.YAMLError as exc:
            print(exc)


    print(type(config))
    #t = """Hello there my name is per second spike and my other name is sharp wave activity"""

    highlighter = Highlighter()
    t = highlighter.highlight_match(sample, config)
    st.markdown(t, unsafe_allow_html=True)


if st.button("Click"):
    main()
