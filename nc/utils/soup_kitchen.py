from bs4 import BeautifulSoup, Comment
from typing import List


class SoupKitchen(object):

    def __init__(self, html: str, parser: str = 'lxml'):
        self.dom = BeautifulSoup(html, parser)

    def purge_comments(self, node=None):
        if not node:
            node = self.dom

        for element in node.findAll(text=lambda text: isinstance(text, Comment)):
            element.extract()

        return node

    def purge_tags(self, tag: str, node=None):
        if not node:
            node = self.dom

        for element in node.findAll(tag):
            element.extract()

        return node

    def purge_scripts(self, node=None):
        return self.purge_tags('script', node)

    def find_id(self, elem: str, name: str):
        return self.dom.find(elem, id=name)

    def find_class(self, elem: str, name: str):
        return self.dom.find(elem, class_=name)

    def split(self, s: str, sep: str) -> tuple:
        return s.split(sep)[0], s.split(sep)[1]

    def find_data_attributes(self, elem: str, attr_name: str, parent=None):
        if not parent:
            parent = self.dom
        return parent.findAll(elem, attrs={attr_name: True})

    def find_recursive(self, selectors: List[str], parent=None):
        node = parent or self.dom

        for s in selectors:
            if '#' in s:
                elem, value = self.split(s, '#')
                node = node.find(elem, id=value)
            elif '.' in s:
                elem, value = self.split(s, '.')
                node = node.find(elem, class_=value)
            else:
                node = node.find(s)

            if not node:
                break

        return node
