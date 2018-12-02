# -*- coding: utf-8 -*-
"""
Crawler for [readlightnovel.org](https://www.readlightnovel.org/).
"""
import logging

from bs4 import BeautifulSoup

from .utils.crawler import Crawler

logger = logging.getLogger('READLIGHTNOVEL')


class ReadLightNovelCrawler(Crawler):
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

        self.novel_title = soup.select_one('.block-title h1').text
        logger.info('Novel title: %s', self.novel_title)

        self.novel_cover = self.absolute_url(
            soup.find('img', {'alt': self.novel_title})['src'])
        logger.info('Novel cover: %s', self.novel_cover)

        try:
            self.novel_author = soup.select_one(
                "a[href*=author]").text.strip().title()
            logger.info('Novel author: %s', self.novel_author)
        except Exception as err:
            logger.debug('Failed getting author: %s', err)
        # end try

        for a in soup.select('.chapters .chapter-chs li a'):
            chap_id = len(self.chapters) + 1
            if len(self.chapters) % 100 == 0:
                vol_id = chap_id // 100 + 1
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({
                    'id': vol_id,
                    'title': vol_title,
                })

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

        body_parts = soup.select_one('.chapter-content3 .desc')
        body = self.extract_contents(body_parts.contents)
        return '<p>' + '</p><p>'.join(body) + '</p>'
