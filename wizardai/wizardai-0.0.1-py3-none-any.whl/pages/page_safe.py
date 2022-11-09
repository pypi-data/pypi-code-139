import streamlit as st
import plotly.graph_objects as go
import time
import pandas as pd
import numpy as np
import matplotlib as mpl
from streamlit import session_state


# ## Fairness
# - Fairness Failure Rate
# - Fairness Impact Score
# - Fairness Across Accuracy

## TODO:
## Smarter coloring of plots
    ## Color + hover could be impact score
    ## Impact score fades for both pos/neg
## xlim/ylims on plots
## "none" color is dependent on streamlit background
## Spot Checking


def app():

    # avg_acc = 89
    # acc_risk_threshold = 7

    def colorFader(c1,c2,mix=0):
        c1=np.array(mpl.colors.to_rgb(c1))
        c2=np.array(mpl.colors.to_rgb(c2))
        return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

    st.title('Fairness Testing')


    st.markdown("### Overall Fairness Score:")
    safe_json = session_state.model_json['safety']
    fair_score = int(safe_json['score'])

    score_bar = st.progress(0)
    st.markdown(f"# {fair_score}%")
    for percent_complete in range(fair_score):
     time.sleep(0.01)
     score_bar.progress(percent_complete + 1)

    # Removing "Target Accuracy" as column bc not in data, need to rethink
    colms = st.columns((1, 1, 1))
    fields = ["","Failure Rate","Impact Score"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)

    for cat in safe_json['tests']:

        # Removing "Target Accuracy" as column bc not in data, need to rethink
        col1, col2, col3  = st.columns((1, 1, 1))

        col1.markdown(f"<h5>{cat}</h5>", unsafe_allow_html=True)

        val = safe_json[cat]['fail_rate']
        style_s = f'background-color:{colorFader("none","red",val)}'
        col2.markdown(f"<h5 style={style_s}>{np.round(val*100,2)}%</h5>",unsafe_allow_html=True)

        val = safe_json[cat]['fail_impact']
        style_s = f'background-color:{colorFader("none","red",min([1,val/(0.25)]))}'
        col3.markdown(f"<h5 style={style_s}>{np.round(val,3)}</h5>",unsafe_allow_html=True)


    st.markdown("---")
    for cat in safe_json['tests']:
        with st.expander(cat):
            subgroup_data = safe_json[cat]["subgroups"]
            subgroup_list = list(subgroup_data['fail_rate'].keys())

            ## FAILURE RATE
            st.markdown("## Swap Failure Rate")
            st.markdown("""
            _The % of times swapping racial adjectives significantly impacted final score (>0.1).
            The_ **prevelance** _of failure_
            """)

            y = [subgroup_data['fail_rate'][i] for i in subgroup_list]
            max_y = 0.5 if max(y) <0.5 else 1.0

            trace1 = go.Bar(x=subgroup_list, y=y,
                        marker=dict(color=[colorFader("none","red",val) for val in y]))

            layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis = dict(title = 'Swap Failure Rate (%)'),
                    yaxis_range=[0,max_y]
            )

            fig = go.Figure(layout = layout, data=trace1)

            st.write(fig)

            st.markdown("## Failure Impact")

            st.markdown("""_The average impact to final score of swapping racial adjectives during testing.
            The_ **magnitude** _of failure_""")

            y = [subgroup_data['fail_impact'][i] for i in subgroup_list]
            trace1 = go.Bar(x=subgroup_list, y=y,
                        marker=dict(color=['orange' if i < 0.1 else 'red' for i in y]))

            layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis = dict(title = 'Failure Impact Score'),
                    yaxis_range=[0,0.5]
            )

            fig = go.Figure(layout = layout, data=trace1)

            st.write(fig)

            st.markdown("## Failure Bias")

            st.markdown("""_The average bias to final score of swapping racial adjectives during testing.
            The_ **direction** _of failure_""")
            st.markdown("""_**NOTE:** If the average bias appears low but the failure impact score is substancial, 
                this mean that model has no overall directional, but significant contextual bias._ """)

            y = [subgroup_data['avg_bias'][i] for i in subgroup_list]
            trace1 = go.Bar(x=subgroup_list, y=y,
                        marker=dict(color=['red' if i < 0 else 'green' for i in y]))

            layout = go.Layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis = dict(title = 'Failure Bias Score'),
                    yaxis_range=[0,0.5]
            )

            fig = go.Figure(layout = layout, data=trace1)

            st.write(fig)

            ## ACC
            # st.markdown("## Accuracy across Protected Groups")
            # st.markdown("""_The accuracy of model segmented by protected groups.
            # The_ **equity** _of model_""")

            # y = [88,92,82]
            # # trace1 = go.Bar(x=race_list, y=y, orientation='h')
            # trace1 = go.Bar(x=y, y=race_list, orientation='h',
            #             marker=dict(
            #             color=[colorFader("none","red",min(1,np.abs(val-avg_acc)/acc_risk_threshold)) for val in y]
            #             ))

            # layout = go.Layout(
            #         paper_bgcolor='rgba(0,0,0,0)',
            #         plot_bgcolor='rgba(0,0,0,0)',
            #         xaxis = dict(title = 'Accuracy'),
            # )

            # fig = go.Figure(layout = layout, data=trace1)

            # fig.add_vline(x=avg_acc,line_dash="dash", line_color="grey")

            # st.write(fig)