#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interactive value input"""
import logging
import os

import requests
from colorama import init as init_colorama

from .app import start_app
from .app.arguments import get_args, build_parser
from .app.display import description, debug_mode
from .assets.version import get_value as get_version
from .tests.crawler_app_test import run_tests
from .crawlers import *

crawler_list = {
    'https://lnmtl.com/': LNMTLCrawler,
    'https://www.webnovel.com/': WebnovelCrawler,
    'https://wuxiaworld.online/': WuxiaOnlineCrawler,
    'https://www.wuxiaworld.com/': WuxiaWorldCrawler,
    'https://www.wuxiaworld.co/': WuxiaCoCrawler,
    'https://boxnovel.com/': BoxNovelCrawler,
    'https://novelplanet.com/': NovelPlanetCrawler,
    'https://www.readlightnovel.org/': ReadLightNovelCrawler,
    'https://lnindo.org/': LnindoCrawler,
    'https://www.idqidian.us/': IdqidianCrawler,
}


def main():
    init_colorama()

    os.environ['version'] = get_version()

    description()
    build_parser()

    args = get_args()
    if args.log:
        os.environ['debug_mode'] = 'true'
        levels = [None, logging.WARN, logging.INFO, logging.DEBUG]
        logging.basicConfig(level=levels[args.log])
        debug_mode(args.log)
        print(args)

    requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)

    try:
        if args.test:
            run_tests()
        else:
            start_app(crawler_list)

    except Exception as err:
        if args.log == 3:
            raise err


if __name__ == '__main__':
    main()
