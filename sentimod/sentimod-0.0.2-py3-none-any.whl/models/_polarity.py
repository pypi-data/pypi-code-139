# import pandas as pd
# from textblob import TextBlob


# def polarity_blob(content: pd.DataFrame) -> float:
#     """polarity using textblob

#     Args:
#         content (pd.DataFrame): _description_

#     Returns:
#         float: _description_
#     """
#     polarity = [0] * len(content)
#     subjectivity = [0] * len(content)

#     # forming a separate feature for cleaned tweets
#     for i, v in enumerate(content["Clean"]):
#         polarity[i] = TextBlob(v).sentiment.polarity
#         subjectivity[i] = TextBlob(v).sentiment.subjectivity

#     content["Polarity"] = polarity
#     content["Subjectivity"] = subjectivity
#     return content
