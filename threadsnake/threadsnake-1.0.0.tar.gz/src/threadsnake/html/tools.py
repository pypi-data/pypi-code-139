from typing import Dict

def tag(name:str, content:str = None, attributes:Dict[str, str] = None, cls=None) -> str:
    result = f'<{name}'
    attributes = attributes or {}
    if cls is not None: attributes['class'] = cls
    attrib:str = ' '.join([f'{i}="{attributes[i]}"' for i in attributes])
    result += attrib
    if content is not None:
        result += '/>'
    else:
        result += '>' + content + f'</{name}>'

def link(location:str, text:str, cls:str = None):
    return tag('a', text, {
        "href": location
    }, cls)