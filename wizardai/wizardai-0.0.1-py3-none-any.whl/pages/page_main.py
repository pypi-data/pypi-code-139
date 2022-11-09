import streamlit as st
import os
import json
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from streamlit import session_state

# ## Summary
# - Reliaibility Score
# - Fairness Score
# - Interpretability Score

## The models/ folder contains all model runs to display here. They contain:
    ## a model.pkl file (helpful for governance and interactivity in report)
    ## a model.json file that contains static test results and model information

def high_risk_counter(j):
    c = 0
    for area in ['safety','performance']:
        area_json = j[area]

        for t in j[area]['tests']:
            if area_json[t]['risk_level'] == 'High':
                c += 1
    return(c)
def app():
    st.title('Model Store')

    model_names = []
    model_types = []
    audit_owners = []
    audit_dates = []
    safe_score = []
    perf_score = []
    high_risk = []
    acc_metrics = []

    ## OS is in demo folder?
    models_repo_path = os.getcwd()+'/full_audit/models'
    for model in os.listdir(models_repo_path):

        ## Skip demo models:
        if model in ["model1","model2",'temp_model3']:
            continue
            
        j = json.load(open(models_repo_path+f"/{model}/{model}.json"))
        model_names.append(j['model_name'])
        model_types.append(j['model_type'])
        audit_owners.append(j['audit_owner'])
        audit_dates.append(j['audit_date'])
        safe_score.append(int(j['safety']['score']))
        perf_score.append(int(j['performance']['score']))
        acc_metrics.append(j['acc'])
        high_risk.append(high_risk_counter(j))

    model_df = pd.DataFrame({
        "View Audit": "",
        "Model Name":model_names,
        "Type": model_types,
        "Owner":audit_owners,
        "Audit Date": audit_dates,
        "Acc Metrics": acc_metrics,
        "Safety Score": safe_score,
        "Performance Score": perf_score,
        "High Risk Areas": high_risk,
        "Deployed": "No",
        })

    gb = GridOptionsBuilder.from_dataframe(model_df)
    gb.configure_selection('single', use_checkbox=True, pre_selected_rows=[len(model_df)-1]) 
    gridOptions = gb.build()

    audit_data = AgGrid(model_df, width='100%',gridOptions=gridOptions,)

    # This is duct tap because an error flashes on screen for a split second and always terrifies me
    try:
        session_state.model_name = audit_data['selected_rows'][0]["Model Name"]
        session_state.model_json= json.load(open(models_repo_path+f"/{session_state.model_name}/{session_state.model_name}.json"))
        st.markdown(f"<h1>{session_state.model_name}</h1>", unsafe_allow_html=True)  
    except IndexError:
        st.write("")

    if "model_name" in session_state:

        st.markdown("---")
        st.markdown("<h2>Accuracy Scores</h2>", unsafe_allow_html=True)  

        summ_stats_name = ['Train ACC',"Train F1","Test ACC","Test F1"]
        summ_stats_vals = [session_state.model_json['accuracy'][i.lower().replace(" ","_")] for i in summ_stats_name]

        for i, stat_name in enumerate(summ_stats_name):
            col1, col2, = st.columns((1, 1))
            col1.write(stat_name)
            col2.write(summ_stats_vals[i])

        st.markdown("---")
        st.markdown("<h2>Safety Tests</h2>", unsafe_allow_html=True)  

        for cat in session_state.model_json['safety']['tests']:
            col1, col2, col3 = st.columns((1, 1, 1))
            col1.write(cat)
            val = session_state.model_json['safety'][cat]['risk_level']

            if val == 'Low':
                style_s = "background-color:transparent"
            elif val == 'Moderate':
                style_s = "background-color:#8b0000"
            else:
                style_s = "background-color:red"

            col2.markdown(f"<h5 style={style_s}>{val} Risk</h5>",unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<h2>Explainability Tests</h2>", unsafe_allow_html=True)

        for cat in ['Local Explainations','Global Explainations']:
            col1, col2, col3 = st.columns((1, 1, 1))
            col1.write(cat)
            col2.markdown("")

            val = col3.selectbox(
            f'{cat.split()[0]} Risk',
            ('Low','Moderate','High'))

            if val == 'Low':
                style_s = "background-color:transparent"
            elif val == 'Moderate':
                style_s = "background-color:#8b0000"
            else:
                style_s = "background-color:red"

            col2.markdown(f"<h5 style={style_s}>{val} Risk</h5>",unsafe_allow_html=True)


        st.markdown("---")
        st.markdown("<h2>Performance Tests</h2>", unsafe_allow_html=True)


        for cat in session_state.model_json['performance']['tests']:
            col1, col2, col3 = st.columns((1, 1, 1))
            col1.write(cat)

            val = session_state.model_json['performance'][cat]['risk_level']
            
            if val == 'Low':
                style_s = "background-color:transparent"
            elif val == 'Moderate':
                style_s = "background-color:#8b0000"
            else:
                style_s = "background-color:red"

            col2.markdown(f"<h5 style={style_s}>{val} Risk</h5>",unsafe_allow_html=True)

        st.markdown("---")
        do_action = st.button("Deploy & Monitor", key="Deploy")
