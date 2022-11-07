""" Placeholder for proverb.py module documentation """

import random

sentence_list = [
    "Le goudron amer de la dignité vaut mieux que le miel de la tranquillité",
    "Qui vous connait petit ne vous respecte pas grand",
    "Qui mange seul s’étrangle seul",
    "Ne dis pas tes peines à autrui, l'épervier et le vautour s'abattent sur le blessé qui gémit",
    "N'ouvre la bouche que si tu es sûr que ce que tu vas dire est plus beau que le silence",
]

def proverbe(text: str, sentence_list: list[str] = sentence_list) -> str:
    """ Analyse text input and select a relevant sentence to return to the user (if applicable)

    Args:
      text: str: text input to be analysed in order to select an appropriate response sentence
      sentence_list: list[str]: list of sentence from which to choose a response (if applicable)

    Returns:
      response: str: an element of the sentence_list

    """
    return random.choice(sentence_list)
