# -*- coding: utf-8 -*-
"""
Crawler for [WuxiaWorld](http://www.wuxiaworld.com/).
"""
import logging

from bs4 import BeautifulSoup

from .crawler import Crawler

logger = logging.getLogger('WUXIA_WORLD')


class WuxiaWorldCrawler(Crawler):
    @property
    def supports_login(self):
        '''Whether the crawler supports login() and logout method'''
        return False

    def login(self, email, password):
        pass

    def logout(self):
        pass

    def read_novel_info(self, url=None):
        '''Get novel title, author, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        response = self.get_response(self.novel_url)
        soup = BeautifulSoup(response.text, 'lxml')

        self.novel_title = soup.select_one('.section-content  h4').text
        logger.info('Novel title: %s', self.novel_title)

        try:
            self.novel_cover = self.absolute_url(
                soup.select_one('img.media-object')['src'])
            logger.info('Novel cover: %s', self.novel_cover)
        except Exception as ex:
            logger.debug('Failed to get cover: %s', ex)

        self.novel_author = soup.select_one('.media-body dl dt').text
        self.novel_author += soup.select_one('.media-body dl dd').text
        logger.info('Novel author: %s', self.novel_author)

        noidungm = soup.select_one('#noidungm')
        if noidungm:
            noidungm.select_one('h2').extract()
            self.novel_summary = noidungm.text

        for panel in soup.select('#accordion .panel-default'):
            vol_id = int(panel.select_one('h4.panel-title .book').text)
            vol_title = panel.select_one('h4.panel-title .title a').text
            self.volumes.append({
                'id': vol_id,
                'title': vol_title,
            })
            for a in panel.select('ul.list-chapters li.chapter-item a'):
                chap_id = len(self.chapters) + 1
                self.chapters.append({
                    'id': chap_id,
                    'volume': vol_id,
                    'url': self.absolute_url(a['href']),
                    'title': a.text.strip() or ('Chapter %d' % chap_id),
                })

        logger.debug(self.chapters)
        logger.debug('%d chapters found', len(self.chapters))

    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        logger.info('Downloading %s', chapter['url'])
        response = self.get_response(chapter['url'])
        soup = BeautifulSoup(response.text, 'lxml')

        self.blacklist_patterns = [
            r'^<span>(...|\u2026)</span>$',
            r'^translat(ed by|or)',
            r'(volume|chapter) .?\d+',
        ]
        body_parts = soup.select_one('.panel-default .fr-view')
        body = self.extract_contents(body_parts.contents)
        return '\n'.join('<p>{}</p>'.format(s) for s in body)
        # return '<p>' + '</p><p>'.join(body) + '</p'
