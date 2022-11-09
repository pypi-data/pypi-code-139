import wizardai.pages.page_main as page_main
import wizardai.pages.page_explain as page_explain
import pwizardai.pages.page_safe as page_safe
import wizardai.pages.page_perf as page_perf
import wizardai.pages.page_repairs as page_repairs
import streamlit as st
import plotly.graph_objects as go
import json
import os
from streamlit import session_state


## Run data, and then save it

## Pull the right pages 
    ## THE PAGES ARE DYNAMIC BASED ON THE AUDIT TYPE !!!!
    ## Solution: A Master dictionary with page names tied to audit type (TODO)

PAGES = {
    "Model Store":page_main,
    "Safety": page_safe,
    "Explainability": page_explain,
    "Performance": page_perf,
    "Repairs & Upgrades": page_repairs
}

st.sidebar.image('/wizardai/assets/wzrd_logo_bluewhite.png', use_column_width=True)
st.sidebar.title('Model Validation')


## This is because this page loads before Model Store, so no audit selected
model_name = ""
train_acc = '';train_f1 = '';test_acc = '';test_f1 = ''
if 'model_name' in session_state:
    model_name = session_state.model_name
    train_acc = session_state.model_json['acc']
    train_f1 = session_state.model_json['f1']
    try:
        test_acc = session_state.model_json['accuracy']['test_acc']
        test_f1 = session_state.model_json['accuracy']['test_acc']
    except:
        do = "nothing"

selection = st.sidebar.radio(model_name, list(PAGES.keys()))
st.sidebar.text(f"Train ACC: {train_acc}")
st.sidebar.text(f"Train F1: {train_f1}")
st.sidebar.text(f"Test ACC: {test_acc}")
st.sidebar.text(f"Test F1: {test_f1}")

page = PAGES[selection]
page.app()
