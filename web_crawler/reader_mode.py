from bs4 import BeautifulSoup as bs
from readability import Document
import requests
import ssl


TO_CHOP_OFF = [' ', '\n', '\t', '\r']
TO_DELETE = ['\n', '\t', '\r', '  ', '/', '\\', '*', '<', '>']

def normalize_text(text_to_normalize):
    normalized_text = text_to_normalize
    
    for symbol in TO_DELETE:
        if symbol in normalized_text:
            normalized_text = normalized_text.replace(symbol, '')

    while normalized_text:
        if any(s == normalized_text[0] for s in TO_CHOP_OFF):
            normalized_text = normalized_text[1:]
        elif any(s == normalized_text[-1] for s in TO_CHOP_OFF):
            normalized_text = normalized_text[:-1]
        else:
            break

    return normalized_text


def reader_mode(html):

    doc = Document(html)
    soup = bs(doc.summary(), 'lxml')
    text = normalize_text(soup.text)
    return text


# with open('testweb.html', 'r', encoding = 'utf-16') as f:
#     html = f.read()

# print(reader_mode(html))
