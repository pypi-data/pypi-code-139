"Chiaki translator module"

from chiaki.exceptions import *
import googletrans

def validate_lang(lang):
    if not lang:
        return True
    if lang in googletrans.LANGUAGES:
        return True
    raise ChiakiBadLangException(lang)
    return False

class Translator(object):

    def __init__(self, source:str, target:str):
        self.tr = googletrans.Translator()
        validate_lang(source)
        validate_lang(target)
        self.source = source
        self.target = target

    def translate(self, text, reverse=False):
        if reverse:
            result = self.tr.translate(
                    text,
                    dest=self.source,
                    src=self.target
                    )
        else:
            result = self.tr.translate(
                    text,
                    src=self.source,
                    dest=self.target
                    )
        return result.text
    
    def retranslate(self, text):
        target = self.translate(
                text = text
                )
        test = self.translate(
                text = target,
                reverse=True
                )
        return target, test

