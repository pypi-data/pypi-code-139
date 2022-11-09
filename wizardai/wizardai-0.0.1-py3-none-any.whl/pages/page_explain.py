import streamlit as st
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import os

## TODO:
## Ploty vs matplotlib
## GbSA
## SHAP
## More Global explainers?
## Hand-picked score?
## Multiple models

#### VADER Model ####
analyzer = SentimentIntensityAnalyzer()

def vader_func(inputs):

    scores = []
    if type(inputs) == str:
        inputs = [inputs]
    for i in inputs:
         polar = analyzer.polarity_scores(i)
         scores.append([polar['neg'],polar['pos']])
    return(np.array(scores))

def explain(model_func,data):
    """
    Parameters
    ---------
    model_func: function
        A function that can take in a list of string sentences
        and return a list of "raw" predictions.
    data: list[str]
        A list of sentences to check scoring
    visual: bool
        A flag for if we want a visual or textual output

    _I don't need labels because I can just run the model myself_

    Output
    -------
    Human-level explaination for datapoint

    """

    # if type(data) == str:
    #     data = [data]

    tokens = nltk.word_tokenize(data)
    tags = nltk.pos_tag(tokens)

    ## TODO cant handle multiple inputs
    real_score = model_func(data)[0]
    broken_sentences = []

    spacing = []
    for word, pos in tags:
        ## TODO: Handle repeated words in sentence
        split = data.split(word)
        broken_sentences.append(split[0]+split[1])

    broke_scores = model_func(broken_sentences)

    ## TODO MINMAX for impact score
    impact_neg = broke_scores[:,0]-real_score[0]
    impact_pos = broke_scores[:,1]-real_score[1]
    impact = -1*(impact_pos-impact_neg)

    fig = plt.figure(figsize=[10,8])

    x = [i for i in range(len(tokens))]

    csfont = {'fontname':'Helvetica'}

    plt.ylim([-0.5,0.5])
    plt.xlim([-0.5,x[-1]+0.5])
    plt.axhline(0,linestyle='--',color='grey')
    plt.axvline(-0.5,linestyle='--',color='grey')


    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().get_xaxis().set_ticks([])
    plt.yticks(ticks=[-0.5,0.5], labels=[str(-0.5),str(0.5)])

    c = []
    for i in x:
        plt.text(i,0.3,tokens[i],ha='center',**csfont,size=15)
        if np.abs(impact[i]) < 0.1:
            c.append('grey')
        elif impact[i] < 0:
            c.append('red')
        else:
            c.append('green')


    plt.bar(x,impact,color=c)

    return(fig)

def app():
    st.title('Explainability Testing ')

    st.markdown("## Spot Checks")

    option = st.selectbox(
            'From Dataset',
            ('I really love my good doctor.', 'I kinda hate Mondays.', 'My mom is really good at soccer.'))

    text_option = st.text_input("Custom Example")

    if text_option == '':
        o = option
    else:
        o = text_option

    st.write('You selected:', o)

    st.write(explain(vader_func,o))

    # st.markdown("## GbSA Auditing + Visuals")
    # st.write("coming soon")

    st.markdown("## Global Explainability")
    st.image(os.getcwd()+'/full_audit/assets/shap_sentiment.png', use_column_width=True)
