import logging
import os
import re

from bs4 import BeautifulSoup
from html2text import html2text

logger = logging.getLogger('TEXT_BINDER')


def _to_txt_ht(s):
    return html2text(s, bodywidth=0)


def _to_txt_bs(s):
    soup = BeautifulSoup(s, 'lxml')
    text = '\n\n'.join(soup.stripped_strings)
    text = re.sub('[\r\n]+', '\r\n', text)
    return text


to_txt = _to_txt_ht


def make_texts(app, data):
    filenames = []
    for vol in data:
        dir_name = os.path.join(app.output_path, 'text', vol)
        os.makedirs(dir_name, exist_ok=True)
        for chap in data[vol]:
            body = chap['body']  # .replace('</p><p', '</p>\n<p')
            content = to_txt(body)
            fname = '{}.txt'.format(str(chap['id']).rjust(5, '0'))
            fname = os.path.join(dir_name, fname)
            with open(fname, 'w', encoding='utf-8') as fp:
                fp.write(content)
            filenames.append(fname)

    logger.warning('Created: %d text files', len(filenames))
    return filenames
