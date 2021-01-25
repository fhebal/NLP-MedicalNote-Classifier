import streamlit as st

from load_css import local_css

local_css("style.css")


class Highlighter():
    def __init__(self):
        self.start = "<span class='highlight blue'><span class='bold'>"
        self.end = "</span></span>"
        self.lookup = ['yo', 'Fanilo']
    def highlight_match(self, text, config):
        for value in self.lookup:
            text = text.replace(value, "{0}"+value+"{1}")
        text = "<div>" + text.format(self.start, self.end) + "</div>"
        return text

import yaml

with open("example.yaml", 'r') as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)

t = """Hello there my name is per second spike and my other name is sharp wave activity"""
highlighter = Highlighter()
t = highlighter.highlight_match(t, config)
st.markdown(t, unsafe_allow_html=True)
