import os
import re
import shutil

from bs4 import BeautifulSoup
from html2text import html2text


# Clear the contents of a directory.
def cleardir(dirpath: str):
    if os.path.isdir(dirpath):
        for name in os.listdir(dirpath):
            path = os.path.join(dirpath, name)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)


# Write a string to a file. Creates parent directories if required.
def writefile(fname: str, content: str):
    fname = os.path.abspath(fname)
    dir_name = os.path.dirname(fname)

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(fname, 'w', encoding='utf-8') as fp:
        fp.write(content)


# HTML to text

def _to_txt_ht(s: str) -> str:
    return html2text(s, bodywidth=0)


def _to_txt_bs(s: str) -> str:
    soup = BeautifulSoup(s, 'lxml')
    text = '\n\n'.join(soup.stripped_strings)
    text = re.sub('[\r\n]+', '\r\n', text)
    return text


to_txt = _to_txt_ht
