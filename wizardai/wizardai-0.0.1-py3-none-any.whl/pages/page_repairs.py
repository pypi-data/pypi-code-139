import streamlit as st
import pandas as pd
from streamlit import session_state
import matplotlib as mpl
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import time

def app():
	st.title('Repairs & Upgrades')

	st.write("""
	_The objective here is to identify data artifacts and pair each artifact with appropriate synthetic data._
	_The synthetic data will ideally mitigate these data artifacts by creating a more uniform dataset._\n\n
	_The cost of this synthetic data is typically a few points of accuracy; and the more synthetic data included, the larger this cost._
	""")


	safe_tests = session_state.model_json['safety']['tests']
	safe_risks = [session_state.model_json['safety'][t]['risk_level'] for t in safe_tests]

	perf_tests = session_state.model_json['performance']['tests']
	perf_risks = [session_state.model_json['performance'][t]['risk_level'] for t in perf_tests]

	cats = ['Safety' for i in safe_tests] + ['Performance' for i in perf_tests]

	rec_data = pd.DataFrame({
	"Artifact":safe_tests+perf_tests,
	"Category": cats,
	"Risk Level":safe_risks + perf_risks})

	gb = GridOptionsBuilder.from_dataframe(rec_data)
	gb.configure_selection('multiple', use_checkbox=True, pre_selected_rows=None) 
	gridOptions = gb.build()

	synth_data = AgGrid(rec_data, width='100%',gridOptions=gridOptions,)

	sel = synth_data['selected_rows']
	if len(sel) >= 1:

		col1, col2,  = st.columns((1, 1,))
		for i in sel:
			col1.write(i['Artifact'])
		col2.write(f"{2500*len(sel):,} synthetic data points")
		col2.button("Generate Synthetic Data", key="synth")
		col2.write("or")
		col2.button("Build Uniform Model", key="model")

	# This is duct tap because an error flashes on screen for a split second and always terrifies me
	# try:
	#     session_state.model_name = audit_data['selected_rows'][0]["Model Name"]
	#     session_state.model_json= json.load(open(models_repo_path+f"/{session_state.model_name}/{session_state.model_name}.json"))
	#     st.markdown(f"<h1>{session_state.model_name}</h1>", unsafe_allow_html=True)  
	# except IndexError:
	#     st.write("")

