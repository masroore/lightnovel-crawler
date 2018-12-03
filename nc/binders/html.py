import logging
import os

from ..utils.template import SimpleTemplate, render
from ..assets.html_style import get_value as get_css_style

logger = logging.getLogger('HTML_BINDER')


def generate_filename(s):
    return '{}.html'.format(str(s).rjust(5, '0'))


def bind_html_chapter(chapter, prev_chapter, next_chapter):
    prev_button = generate_filename(prev_chapter['id']) if prev_chapter else '#'
    next_button = generate_filename(next_chapter['id']) if next_chapter else '#'
    file_name = generate_filename(chapter['id'])
    tpl_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    tpl = SimpleTemplate(name='html_chapter', lookup=[tpl_dir])
    html = render(tpl,
                  title=chapter['title'],
                  body=chapter['body'],
                  style=get_css_style(),
                  prev_button=prev_button,
                  next_button=next_button)
    return html, file_name


def bind_html_index(title, chapters, dir_name):
    tpl_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    tpl = SimpleTemplate(name='html_index', lookup=[tpl_dir])
    html = render(tpl,
                  title=title,
                  chapters=chapters,
                  style=get_css_style()
                  )
    file_name = os.path.join(dir_name, '00-index.html')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html)
    return html, file_name


def make_htmls(app, data):
    web_files = []
    chapters = []
    for vol in data:
        dir_name = os.path.join(app.output_path, 'html', vol)
        os.makedirs(dir_name, exist_ok=True)
        for i in range(len(data[vol])):
            chapter = data[vol][i]
            prev_chapter = data[vol][i - 1] if i > 0 else None
            next_chapter = data[vol][i + 1] if i + 1 < len(data[vol]) else None
            html, file_name = bind_html_chapter(chapter, prev_chapter, next_chapter)

            chapters.append({'title': chapter['title'], 'link': './{0}'.format(file_name)})
            file_name = os.path.join(dir_name, file_name)
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(html)

            web_files.append(file_name)

    bind_html_index(app.crawler.novel_title, chapters, os.path.join(app.output_path, 'html'))

    logger.warning('Created: %d html files', len(web_files))
    return web_files
