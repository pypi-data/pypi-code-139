import os

import streamlit.components.v1 as components

# Now the React interface only accepts an array of 1 or 2 elements.
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/dist")
_component_func = components.declare_component("st_dataframe_component", path=build_dir)


# Edit arguments sent and result received from React component, so the initial input is converted to an array and returned value extracted from the component
def st_custom_slider(data) -> int:
	component_value = _component_func(data=data)
	return component_value
