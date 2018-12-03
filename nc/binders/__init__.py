# -*- coding: utf-8 -*-
"""
To bind into ebooks
"""
import logging
from typing import Dict

from .epub import make_epubs
from .html import make_htmls
from .mobi import make_mobis
from .text import make_texts
from .zbook import make_zbooks
from ..core.program import Program

logger = logging.Logger('BINDERS')


def make_data(prog: Program) -> Dict:
    data = {}
    if prog.pack_by_volume:
        for vol in prog.crawler.volumes:
            data['Volume %d' % vol['id']] = [
                x for x in prog.chapters if x['volume'] == vol['id'] and len(x['body']) > 0
            ]

    else:
        data[''] = prog.chapters

    return data


def bind_books(prog: Program):
    data = make_data(prog)
    make_zbooks(prog, data)
    make_texts(prog, data)
    make_htmls(prog, data)
    epubs = make_epubs(prog, data)
    make_mobis(prog, epubs)
