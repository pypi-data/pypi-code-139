import os

import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
	_component_func = components.declare_component(
	    "st_dataframe_component",
	    url="http://localhost:3001",
	)
else:
	parent_dir = os.path.dirname(os.path.abspath(__file__))
	build_dir = os.path.join(parent_dir, "frontend/build")
	_component_func = components.declare_component("st_dataframe_component", path=build_dir)


def st_custom_dataframe(data) -> int:
	component_value = _component_func(data=data)
	return component_value