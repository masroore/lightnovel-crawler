import json
import logging
import os
from zipfile import ZipFile, ZIP_DEFLATED

from ..utils.helpers import to_txt

logger = logging.getLogger('TEXT_BINDER')


class Zbook(object):

    def __init__(self, filename, title, author, cover):
        self.filename = filename
        self.title = title
        self.author = author
        self.cover = cover
        self.toc = []

        self._zf = ZipFile(filename, mode='w')
        self._compress_type = ZIP_DEFLATED
        self._compress_level = 9

        if cover and os.path.isfile(cover):
            dest_name = 'resources/cover.jpg'
            self._zf.write(self.cover, dest_name)
            self.cover = dest_name

    def __str__(self):
        props = {'title': self.title, 'author': self.author, 'toc': self.toc}
        return json.dumps(props, indent=4)

    def _write(self, fname, content):
        self._zf.writestr(fname, content, compress_type=self._compress_type, compresslevel=self._compress_level)

    def close(self):
        self._write('manifest.json', str(self))
        self._zf.close()
        del self._zf

    def add_chapter(self, chapter_id, volume, title, content):
        fname = 'resources/chap_{}.txt'.format(chapter_id.rjust(5, '0'))
        self.toc.append({'id': chapter_id, 'volume': volume, 'title': title, 'file': fname})
        self._write(fname, to_txt(content))


def bind_zb_volume(app, chapters, volume=''):
    book_title = (app.crawler.novel_title + ' ' + volume).strip()
    zbk_dir = os.path.join(app.output_path, 'zbook')
    zbk_basename = book_title + '.zip'
    zbk_fname = os.path.join(zbk_dir, zbk_basename)
    os.makedirs(zbk_dir, exist_ok=True)

    logger.debug('Binding %s', zbk_basename)

    book = Zbook(zbk_fname, book_title, app.crawler.novel_author, app.book_cover)

    for i, chapter in enumerate(chapters):
        book.add_chapter(chapter_id=str(i + 1),
                         volume=volume,
                         title=chapter['title'],
                         content=chapter['body'] or '')
    book.close()

    logger.warning('Created: %s', zbk_basename)
    return zbk_fname


def make_zbooks(app, data):
    zb_files = []
    for vol in data:
        if len(data[vol]) > 0:
            book = bind_zb_volume(app, volume=vol, chapters=data[vol])
            zb_files.append(book)

    logger.warning('Created: %d zbook files', len(zb_files))
    return zb_files
