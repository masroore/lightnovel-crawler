# -*- coding: utf-8 -*-
"""
Crawler application
"""
import re
from concurrent import futures

from ..utils import cfscrape


class Crawler:
    '''Blueprint for creating new spiders'''

    home_url = ''
    novel_url = ''
    last_visited_url = None
    scraper = cfscrape.create_scraper()
    executor = futures.ThreadPoolExecutor(max_workers=5)

    '''Must resolve these fields inside `read_novel_info`'''
    novel_title = 'N/A'
    novel_author = 'N/A'
    novel_cover = None
    novel_summary = None

    '''
    Each item must contain these keys:
    `title` - the title of the volume
    '''
    volumes = []

    '''
    Each item must contain these keys:
    `id` - the index of the chapter
    `title` - the title name
    `volume` - the volume id of this chapter
    `url` - the link where to download the chapter
    `name` - the chapter name, e.g: 'Chapter 3' or 'Chapter 12 (Special)'
    '''
    chapters = []

    def __init__(self):
        self.scraper.verify = False

    # ------------------------------------------------------------------------- #
    # Implement these methods
    # ------------------------------------------------------------------------- #

    def initialize(self):
        pass

    def dispose(self):
        pass

    @property
    def supports_login(self):
        '''Whether the crawler supports login() and logout method'''
        return False

    def login(self, email, password):
        pass

    def logout(self):
        pass

    def read_novel_info(self, url):
        '''Get novel title, autor, cover etc'''
        pass

    def download_chapter_list(self):
        '''Download list of chapters and volumes.'''
        pass

    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        pass

    def get_chapter_index_of(self, url):
        '''Return the index of chapter by given url or 0'''
        url = (url or '').strip().strip('/')
        for chapter in self.chapters:
            if chapter['url'] == url:
                return chapter['id']

        return 0

    # ------------------------------------------------------------------------- #
    # Helper methods to be used
    # ------------------------------------------------------------------------- #
    @property
    def headers(self):
        return self.scraper.headers.copy()

    @property
    def cookies(self):
        return {x.name: x.value for x in self.scraper.cookies}

    def absolute_url(self, url):
        if not url or len(url) == 0:
            return None
        elif url.startswith('//'):
            return 'http:' + url
        elif url.find('//') >= 0:
            return url
        elif url.startswith('/'):
            return self.home_url + url
        else:
            return (self.last_visited_url or self.home_url) + '/' + url

    def get_response(self, url, incognito=False):
        self.last_visited_url = url.strip('/')
        response = self.scraper.get(url)
        response.encoding = 'utf-8'
        self.cookies.update({
            x.name: x.value
            for x in response.cookies
        })
        return response

    def submit_form(self, url, multipart=False, headers={}, **data):
        '''Submit a form using post request'''
        headers = {
            'content-type': 'multipart/form-data' if multipart
            else 'application/x-www-form-urlencoded'
        }
        response = self.scraper.post(url, data=data, headers=headers)
        self.cookies.update({
            x.name: x.value
            for x in response.cookies
        })
        return response

    def download_cover(self, output_file):
        response = self.get_response(self.novel_cover)
        with open(output_file, 'wb') as f:
            f.write(response.content)
        # end with

    blacklist_patterns = [
        r'^(volume|chapter) .?\d+$',
    ]

    def not_blacklisted(self, text):
        for pattern in self.blacklist_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False

        return True

    def extract_contents(self, contents, level=0):
        body = []
        for elem in contents:
            if ['script', 'iframe', 'form', 'a', 'br', 'img'].count(elem.name):
                continue
            elif ['h3', 'div', 'p'].count(elem.name):
                body += self.extract_contents(elem.contents, level + 1)
                continue

            if not elem.name:
                text = str(elem).strip()
            else:
                text = '<%s>%s</%s>' % (elem.name, elem.text.strip(), elem.name)

            patterns = [
                re.compile(r'<!--(.|\n)*-->', re.MULTILINE),
                re.compile(r'\[if (.|\n)*!\[endif\]', re.MULTILINE),
            ]
            for x in patterns:
                text = x.sub('', text).strip()

            if text:
                body.append(text)

        if level == 0:
            return [x for x in body if len(x) and self.not_blacklisted(x)]
        else:
            return body
