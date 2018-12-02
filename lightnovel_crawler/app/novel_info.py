# -*- coding: utf-8 -*-
"""
To get the novel info
"""
import json
import os
import re
import shutil

from .prompts import force_replace_old


def format_volume_list(crawler):
    for vol in crawler.volumes:
        vol['chapter_count'] = 0
        title = 'Volume %d' % vol['id']
        vol['title'] = vol['title'] or title
        if not re.search(r'vol(ume)? .?\d+', vol['title'], re.IGNORECASE):
            vol['title'] = title + ' - ' + vol['title'].title()


def format_chapter_list(crawler):
    for item in crawler.chapters:
        title = 'Chapter #%d' % item['id']
        item['title'] = item['title'] or title
        if not re.search(r'ch(apter)? .?\d+', item['title'], re.IGNORECASE):
            item['title'] = title + ' - ' + item['title'].title()

        item['volume'] = item['volume'] or (1 + (item['id'] - 1) // 100)
        item['volume_title'] = 'Volume %d' % item['volume']
        for vol in crawler.volumes:
            if vol['id'] == item['volume']:
                item['volume_title'] = vol['title']
                vol['chapter_count'] += 1
                break


def save_metadata(crawler, output_path):
    file_name = os.path.join(output_path, 'meta.json')
    data = {
        'title': crawler.novel_title,
        'author': crawler.novel_author,
        'cover': crawler.novel_cover,
        'volumes': crawler.volumes,
        'chapters': crawler.chapters,
    }
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2)


def novel_info(app):
    app.logger.warn('Retrieving novel info...')
    app.crawler.read_novel_info()

    app.logger.info('Checking output path...')
    app.output_path = os.path.abspath(
        re.sub(r'[\\/*?:"<>|\']', '', app.crawler.novel_title))
    if os.path.exists(app.output_path):
        if force_replace_old():
            shutil.rmtree(app.output_path, ignore_errors=True)

    os.makedirs(app.output_path, exist_ok=True)

    app.logger.info('Getting chapters...')
    app.crawler.download_chapter_list()

    format_volume_list(app.crawler)
    format_chapter_list(app.crawler)

    save_metadata(app.crawler, app.output_path)
