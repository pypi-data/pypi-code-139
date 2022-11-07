import os
from enum import Enum
from typing import List, Type, cast

import requests
from pydantic import Field, BaseModel
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText

DEEPL_URL = os.environ.get("DEEPL_URL", "https://api.deepl.com/v2/translate")
DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

deepl_session = requests.Session()
deepl_session.headers.update({"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"})


class TargetLang(str, Enum):
    # BG - Bulgarian
    # CS - Czech
    # DA - Danish
    DE = "DE"
    # EL - Greek
    EN_GB = "EN-GB"
    EN_US = "EN-US"
    ES = "ES"
    # ET - Estonian
    # FI - Finnish
    FR = "FR"
    # HU - Hungarian
    # ID - Indonesian
    IT = "FR"
    # JA - Japanese
    # LT - Lithuanian
    # LV - Latvian
    NL = "NL"
    # PL - Polish
    PT_BR = "PT-BR"
    PT_PT = "PT-PT"
    # RO - Romanian
    RU = "RU"
    # SK - Slovak
    # SL - Slovenian
    # SV - Swedish
    # TR - Turkish
    # UK - Ukrainian
    ZH = "ZH"


class Formality(str, Enum):
    default = "default"
    more = "more"
    less = "less"
    prefer_more = "prefer_more"
    prefer_less = "prefer_less"


class DeepLParameters(ProcessorParameters):
    target_lang: TargetLang = Field(
        None,
        description="""The language into which the text should be translated. Options currently available:</br>
                        <li>`DE` - German
                        <li>`EN-GB` - English (British)
                        <li>`EN-US` - English (American)
                        <li>`ES` - Spanish
                        <li>`FR` - French
                        <li>`IT` - Italian
                        <li>`NL` - Dutch
                        <li>`PT-BR` - Portuguese (Brazilian)
                        <li>`PT-PT` - Portuguese (all Portuguese varieties excluding Brazilian Portuguese)
                        <li>`RU` - Russian
                        <li>`ZH` - Chinese (simplified)""")
    formality: Formality = Field(
        Formality.default,
        description="""Sets whether the translated text should lean towards formal or informal language.
                        This feature currently only works for target languages
                        DE (German), FR (French), IT (Italian), ES (Spanish), NL (Dutch), PL (Polish),
                        PT-PT, PT-BR (Portuguese) and RU (Russian).
                        Setting this parameter with a target language that does not support formality will fail,
                        unless one of the prefer_... options are used. Possible options are:</br>
                        <li>`default` - default
                        <li>`more` - for a more formal language
                        <li>`less` - for a more informal language
                        <li>`prefer_more` - for a more formal language if available, otherwise fallback to default formality
                        <li>`prefer_less` - for a more informal language if available, otherwise fallback to default formality""")
    as_altText: str = Field(
        None,
        description="""If defined generate the translation as an alternative text of the input document,
    if not replace the text of the input document.""",
    )


SUPPORTED_LANGUAGES = (
    "bg,cs,da,de,el,en,es,et,fi,fr,hu,id,it,ja,lt,lv,nl,pl,pt,ro,ru,sk,sl,sv,tr,uk,zh"
)


class DeepLProcessor(ProcessorBase):
    (
        """Translate using DeepL
    #languages:""" + SUPPORTED_LANGUAGES
    )

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)

        params: DeepLParameters = cast(DeepLParameters, parameters)
        try:
            for document in documents:
                lang = document_language(document, None)
                if lang is None or lang not in supported_languages:
                    raise AttributeError(
                        f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}"
                    )
                if document.sentences:
                    stexts = [
                        document.text[s.start:s.end] for s in document.sentences
                    ]
                    trans_texts = [
                        deepl_translate(lang, params.target_lang.value, stext, split_sentences=False)
                        for stext in stexts
                    ]
                    trans_text = "\n".join(trans_texts)
                else:
                    trans_text = deepl_translate(
                        lang, params.target_lang.value, document.text
                    )
                if params.as_altText is not None and len(params.as_altText):
                    document.altTexts = document.altTexts or []
                    altTexts = [
                        alt
                        for alt in document.altTexts
                        if alt.name != params.as_altText
                    ]
                    altTexts.append(AltText(name=params.as_altText, text=trans_text))
                    document.altTexts = altTexts
                else:
                    document.text = trans_text
                    document.metadata["language"] = params.target_lang.value.lower()
                    document.sentences = []
                    document.annotations = None
                    document.categories = None

        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepLParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and "language" in doc.metadata:
        return doc.metadata["language"]
    return default


def deepl_translate(from_lang, to_lang, text, split_sentences=True):
    querystring = {
        "text": text,
        "target_lang": to_lang.upper(),
        "split_sentences": "1" if split_sentences else "0",
        "preserve_formatting": "1",
    }
    if from_lang is not None:
        querystring["source_lang"] = from_lang.upper()

    r = deepl_session.get(DEEPL_URL, params=querystring)
    if r.ok:
        trans = r.json()
        if "translations" in trans:
            return trans["translations"][0]["text"]
    return None
