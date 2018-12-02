# -*- coding: utf-8 -*-
"""
To download chapter bodies
"""
import json
import os
from concurrent import futures
from urllib.parse import urlparse

from progress.bar import IncrementalBar


def download_cover(app):
    app.book_cover = None
    if app.crawler.novel_cover:
        app.logger.warn('Getting cover image...')
        try:
            ext = urlparse(app.crawler.novel_cover).path.split('.')[-1]
            filename = os.path.join(app.output_path, 'cover.%s' % (ext or 'png'))
            if not os.path.exists(filename):
                app.logger.info('Downloading cover image')
                app.crawler.download_cover(filename)
                app.logger.info('Saved cover: %s', filename)
                app.book_cover = filename

        except Exception as ex:
            app.logger.error('Failed to get cover: %s', ex)

    else:
        app.logger.warn('No cover image.')


def download_chapter_body(app, chapter):
    result = None

    dir_name = os.path.join(app.output_path, 'json')
    if app.pack_by_volume:
        dir_name = os.path.join(dir_name,
                                'Volume ' + str(chapter['volume']).rjust(2, '0'))

    os.makedirs(dir_name, exist_ok=True)

    chapter_name = str(chapter['id']).rjust(5, '0')
    file_name = os.path.join(dir_name, chapter_name + '.json')

    chapter['body'] = ''
    if os.path.exists(file_name):
        app.logger.info('Restoring from %s', file_name)
        with open(file_name, 'r') as file:
            old_chapter = json.load(file)
            chapter['body'] = old_chapter['body']

    if len(chapter['body']) == 0:
        body = ''
        try:
            app.logger.info('Downloading to %s', file_name)
            body = app.crawler.download_chapter_body(chapter)
        except Exception as err:
            app.logger.debug(err)

        if len(body) == 0:
            body = result = 'Body is empty: ' + chapter['url']

        chapter['body'] = '<h3>%s</h3><h1>%s</h1>\n%s' % (chapter['volume_title'], chapter['title'], body)
        with open(file_name, 'w') as file:
            file.write(json.dumps(chapter))

    return result


def download_chapters(app):
    download_cover(app)

    bar = IncrementalBar('Downloading chapters', max=len(app.chapters))
    bar.start()
    if os.getenv('debug_mode') == 'true':
        bar.next = lambda: None

    futures_to_check = {
        app.crawler.executor.submit(
            download_chapter_body,
            app,
            chapter,
        ): str(chapter['id'])
        for chapter in app.chapters
    }
    for future in futures.as_completed(futures_to_check):
        result = future.result()
        if result:
            bar.clearln()
            app.logger.error(result)

        bar.next()

    bar.finish()
