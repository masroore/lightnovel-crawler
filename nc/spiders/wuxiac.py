# -*- coding: utf-8 -*-
"""
Crawler for [WuxiaWorld](http://www.wuxiaworld.com/).
"""
import logging
import re

from bs4 import BeautifulSoup

from .crawler import Crawler

logger = logging.getLogger('WUXIA_WORLD')


class WuxiaCoCrawler(Crawler):
    @property
    def supports_login(self):
        '''Whether the crawler supports login() and logout method'''
        return False

    def login(self, email, password):
        pass

    def logout(self):
        pass

    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        response = self.get_response(self.novel_url)
        soup = BeautifulSoup(response.text, 'lxml')

        self.novel_title = soup.select_one('#maininfo h1').text
        logger.info('Novel title: %s', self.novel_title)

        self.novel_author = soup.select_one('#maininfo p').text.strip()
        self.novel_author = re.sub(
            r'^Author[^\w]+', '', self.novel_author).strip()
        logger.info('Novel author: %s', self.novel_author)

        self.novel_cover = self.absolute_url(
            soup.select_one('#sidebar img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)

        last_vol = -1
        volume = {'id': 0, 'title': 'Volume 1', }
        for item in soup.select('#list dl *'):
            if item.name == 'dt':
                vol = volume.copy()
                vol['id'] += 1
                vol['title'] = item.text.strip()
                vol['title'] = re.sub(r'^(.*)', '', vol['title'])
                vol['title'] = re.sub(
                    r'^\s*Text\s*$', '', vol['title']).strip()
                volume = vol

            if item.name == 'dd':
                a = item.select_one('a')
                chap_id = len(self.chapters) + 1
                self.chapters.append({
                    'id': chap_id,
                    'volume': volume['id'],
                    'title': a.text.strip(),
                    'url': self.absolute_url(a['href']),
                })
                if last_vol != volume['id']:
                    last_vol = volume['id']
                    self.volumes.append(volume)

        logger.debug(self.volumes)
        logger.debug(self.chapters)
        logger.debug('%d chapters found', len(self.chapters))

    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        logger.info('Downloading %s', chapter['url'])
        response = self.get_response(chapter['url'])
        soup = BeautifulSoup(response.text, 'lxml')

        self.blacklist_patterns = [
            r'^translat(ed by|or)',
            r'(volume|chapter) .?\d+',
        ]
        body_parts = soup.select_one('div#content').contents
        body = self.extract_contents(body_parts)
        return '<p>' + '</p><p>'.join(body) + '</p>'
