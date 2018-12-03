import logging
import os

from ..utils.helpers import writefile, to_txt

logger = logging.getLogger('TEXT_BINDER')


def make_texts(app, data):
    filenames = []
    for vol in data:
        for chap in data[vol]:
            content = to_txt(chap['body'])
            fname = os.path.join(os.path.join(app.output_path, 'text', vol),
                                 '{}.txt'.format(str(chap['id']).rjust(5, '0')))
            writefile(fname, content)
            filenames.append(fname)

    logger.warning('Created: %d text files', len(filenames))
    return filenames
