# **Twitter Preprocessing Unit**
# remove urls
# remove usernames
# remove hashtags
# character normalization
# Punctuation, special characters and numbers
# Lower casing
import preprocessor as p
import pandas as pd


def cleaner(content: pd.DataFrame):
    """clean the tweets with basic twitter preprocessor

    Args:
        content (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """
    clean = [0] * len(content)

    # forming a separate feature for cleaned tweets
    for i, v in enumerate(content["Text"]):
        # tweets.loc[v,"Text"] = p.clean(i)
        clean[i] = p.clean(v)

    content["Clean"] = clean
    return content
