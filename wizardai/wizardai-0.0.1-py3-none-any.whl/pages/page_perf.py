import streamlit as st
import pandas as pd
from streamlit import session_state
import matplotlib as mpl
import numpy as np
import time
import json

# ## Reliability
# - Typos
# - Synonyms
# - Antonyms

def display_tests(view):
    st.write(view)

    if view == 'Reducers':
        st.markdown(f"""
            Out of `2500` test cases, **{session_state.model_name}** failed to reduce label score by threshold on `1400` (`56.5%`)
            examples
            """)
        
        st.markdown("---")
        colms = st.columns((1, 1))
        st.markdown("<h2>Prototypical Success</h2>", unsafe_allow_html=True)
        suc = ['generally','kinda','probably']
        for i in range(len(suc)):
            col1, col2 = st.columns((1, 1))
            col1.markdown(f"<h4>{suc[i]}</h4>", unsafe_allow_html=True)
            col2.write(str(np.random.randint(0,44))+"% failure rate")
            st.markdown(f"_I *{suc[i]}* like my new doctor._")

        st.markdown("---")
        st.markdown("<h2>Prototypical Failures</h2>", unsafe_allow_html=True)
        fail = ['a little', 'a bit', 'slightly']

        for i in range(len(fail)):
            col1, col2 = st.columns((1, 1))
            col1.markdown(f"<h4>{fail[i]}</h4>", unsafe_allow_html=True)
            col2.write(str(np.random.randint(75,100))+"% failure rate")
            st.markdown(f"_My new apartment is *{fail[i]}* terrible._")



def colorFader(c1,c2,mix=0):
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

def app():
    st.title('Performance Testing')

    perf_json = session_state.model_json['performance']
    perf_score = int(perf_json['score'])

    st.markdown("### Overall Performance Score:")
    if 'rely_bar_done' in session_state:
        score_bar = st.progress(perf_score)
        st.markdown(f"# {perf_score}%")
    else:
        score_bar = st.progress(0)
        st.markdown(f"# {perf_score}%")
        for percent_complete in range(perf_score):
            time.sleep(0.01)
            score_bar.progress(percent_complete + 1)
        session_state.rely_bar_done = True

    
    tests = perf_json['tests']

    f_rate = [perf_json[t]['fail_rate'] for t in tests]
    f_impact = [perf_json[t]['fail_impact'] for t in tests]
    f_impact = [i if i == i else 0 for i in f_impact]

    reliable_df = pd.DataFrame({
        "Test":tests,
        "Failure Rate":f_rate,
        "Failure Impact":f_impact,
        "enabled": False
        })

    colms = st.columns((1, 1, 1, 1 ))
    fields = ["","Test","Failure Rate","Failure Impact"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)

    for x, test in enumerate(reliable_df['Test']):
        col1, col2, col3, col4 = st.columns((1, 1, 1, 1))
        test_name = reliable_df['Test'][x]

        status = reliable_df['enabled'][x] 
        button_type = "" if status else "View"
        button_phold = col1.empty()  # create a placeholder
        do_action = button_phold.button(button_type, key=test_name)

        col2.markdown(f"<h5>{test_name}</h5>",unsafe_allow_html=True)

        val = reliable_df["Failure Rate"][x]
        style_s  = f'background-color:{colorFader("none","red",val)}'  
        col3.markdown(f"<h5 style={style_s}>"+str(np.round(val*100,2))+"%</h5>", unsafe_allow_html=True) 

        val = reliable_df["Failure Impact"][x]
        style_s  = f'background-color:{colorFader("none","red",min([1,val/(0.25)]))}'  
        col4.markdown(f"<h5 style={style_s}>"+str(round(val,3))+"</h5>", unsafe_allow_html=True)  
        
        if do_action:
             session_state.perf_view = test_name
             button_phold.empty()  #  remove button

    if 'perf_view' in session_state:
        st.header(session_state.perf_view)

        test_json = perf_json[session_state.perf_view]

        st.write(f"""After running `{test_json['num_cases']:,}` test cases, 
            this model failed `{int(test_json['num_cases']*test_json['fail_rate']):,}` 
            of these cases (`{100*test_json['fail_rate']:.2f}%`) """)

        ## Tech Debt of our I quickly added examples
        for e in ['pass','fail']:
            if e == 'pass':
                st.markdown(f"<h3>Passed Test Case Examples</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3>Failed Test Case Examples</h3>", unsafe_allow_html=True)

            if test_json['examples'][e][0] != '{':
                st.write("N/A")
            else:

                pass_examples = json.loads(test_json['examples'][e])
                pass_ids = pass_examples['testinput']

                colms = st.columns((1, 1, 1))
                fields = ["Input","Model Output", "Results"]
                for col, field_name in zip(colms, fields):
                    col.write(field_name)

                for id_ in pass_ids:

                    col1, col2, col3 = st.columns((1, 1, 1))
                    ## Single example tests exception
                    if session_state.perf_view in ['Single Negative','Single Positive']:
                        i_pd = pass_examples['testinput'][id_]
                        o_pd = pass_examples['testoutput'][id_]
                        s_pd = e
                    else:
                        i_pd = pd.DataFrame(pass_examples['testinput'][id_])
                        i_pd.columns = [""]
                        i_pd.index = ["baseline","testcase"]

                        o_pd = pd.DataFrame(pass_examples['testoutput'][id_])
                        o_pd.columns = ['neg','pos']
                        o_pd.index = ['',' ']
                        s_pd = pass_examples['testscore'][id_]


                    col1.write(i_pd)
                    col2.write(o_pd)
                    col3.write(s_pd)
        

        # fail_examples = json.loads(test_json['examples']['fail'])

        # if 'testinput' in pass_examples:
        #     pass_ids = pass_examples['testinput']
        # else:
        #     pass_ids = 'NA'
        # if 'testinput' in fail_examples:
        #     fail_ids = fail_examples['testinput']
        # else:
        #     fail_ids = 'NA'

        # st.markdown(f"<h2>Passed Test Case Examples</h2>", unsafe_allow_html=True)
        
        # colms = st.columns((1, 1, 1))
        # fields = ["Input","Model Output", "Results"]
        
        # for col, field_name in zip(colms, fields):
        #     col.write(field_name)

        # for id_ in pass_ids:

        #     col1, col2, col3 = st.columns((1, 1, 1))
        #     i_pd = pd.DataFrame(pass_examples['testinput'][id_])
        #     i_pd.columns = [""]
        #     i_pd.index = ["baseline","testcase"]

        #     o_pd = pd.DataFrame(pass_examples['testoutput'][id_])
        #     o_pd.columns = ['neg','pos']
        #     o_pd.index = ['',' ']


        #     col1.write(i_pd)
        #     col2.write(o_pd)
        #     col3.write(pass_examples['testscore'][id_])

        # st.markdown(f"<h4>Failed Test Case Examples</h4>", unsafe_allow_html=True)

        # for ex_ids in pass_examples['testinput']:

        # for testinput, testoutput, testscore in zip(pass_examples['testinput'],pass_examples['testoutput'],pass_examples['testscore']):
        #     st.write(testinput)
            # st.write(testoutput)
            # st.write(testscore)




        # display_tests(session_state.perf_view)
