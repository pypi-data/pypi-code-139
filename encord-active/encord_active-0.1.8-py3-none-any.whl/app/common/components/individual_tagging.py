import pandas as pd
import streamlit as st
from pandas import Series

import encord_active.app.common.state as state
from encord_active.app.db.merged_metrics import MergedMetrics
from encord_active.app.db.tags import Tags


def update_image_tags(identifier: str, key: str):
    tags = st.session_state[key]
    st.session_state[state.MERGED_DATAFRAME].at[identifier, "tags"] = tags
    MergedMetrics().update_tags(identifier, tags)


def multiselect_tag(row: Series, key_prefix: str):
    identifier = row["identifier"]
    tag_status = st.session_state[state.MERGED_DATAFRAME].at[identifier, "tags"]

    if not isinstance(identifier, str):
        st.error("Multiple rows with the same identifier were found. Please create a new issue.")
        return

    key = f"{key_prefix}_multiselect_{identifier}"

    st.multiselect(
        label="Tag image",
        options=st.session_state.get(state.ALL_TAGS) or [],
        default=tag_status or None,
        key=key,
        label_visibility="collapsed",
        on_change=update_image_tags,
        args=(identifier, key),
    )


def tag_creator():
    with st.sidebar:
        with st.form(key="tag_creator_form"):

            left, middle, right = st.columns((2, 5, 1))
            left.markdown("**Tag name:**")
            tag_name = middle.text_input("tag name", label_visibility="collapsed", key="input_text_tag")
            tag_add_button = right.form_submit_button("+")

            all_tags = Tags().all()

            if tag_add_button:
                if tag_name == "":
                    st.info("Please enter a tag")
                elif tag_name in all_tags:
                    st.info("Tag is already in project tags")
                else:
                    all_tags.append(tag_name)
                    Tags().create_tag(tag_name)

            st.session_state[state.ALL_TAGS] = all_tags

        if not all_tags:
            return

        tags_sum = []
        for tag in all_tags:
            total_tags = len([True for x in st.session_state[state.MERGED_DATAFRAME]["tags"] if tag in x])
            tags_sum.append(total_tags)

        tags_dict = {"Tags": all_tags, "Count": tags_sum}
        st.dataframe(pd.DataFrame(tags_dict), use_container_width=True)
