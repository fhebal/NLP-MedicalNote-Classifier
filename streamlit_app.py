import streamlit as st
import yaml
from load_css import local_css

local_css("style.css")


keys = {
        'Gastroenterology': 0,

        }

option = st.radio("Press the button", [0, 1, 2, 3, 4])
option = 


class Highlighter():
    def __init__(self):
        self.start = "<span class='highlight blue'><span class='bold'>"
        self.end = "</span></span>"
    def highlight_match(self, text, config):
        for value in config:
            text = text.replace(value, "{0}"+value+"{1}")
        text = "<div>" + text.format(self.start, self.end) + "</div>"
        return text


label = 1
with open("config/{}.yaml".format(label), 'r') as stream:
    try:
        config = stream.read().splitlines()
    except yaml.YAMLError as exc:
        print(exc)


print(type(config))
t = """Hello there my name is per second spike and my other name is sharp wave activity"""
highlighter = Highlighter()
t = highlighter.highlight_match(t, config)
st.markdown(t, unsafe_allow_html=True)
