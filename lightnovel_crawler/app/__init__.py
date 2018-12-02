# -*- coding: utf-8 -*-
"""
Interactive application to take user inputs
"""
from .display import url_not_recognized, cancel_method
from .program import Program
from .prompts import get_novel_url


def start_app(choice_list):
    cancel_method()

    novel_url = get_novel_url()

    instance = None
    for home_url, crawler in choice_list.items():
        if novel_url.startswith(home_url):
            instance = crawler()
            instance.novel_url = novel_url
            instance.home_url = home_url.strip('/')
            break

    if not instance:
        url_not_recognized(choice_list)
        return

    Program().run(instance)
