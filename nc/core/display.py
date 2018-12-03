import os

from colorama import Fore, Style

from .icons import Icons

LINE_SIZE = 64


def description():
    print('=' * LINE_SIZE)

    title = Icons.BOOK + ' Novel Crawler ' + \
            Icons.CLOVER + os.environ['version']
    padding = ' ' * ((LINE_SIZE - len(title)) // 2)
    print(Fore.YELLOW, padding + title, Fore.RESET)

    desc = 'Download web novels into html, text, epub, mobi and json'
    padding = ' ' * ((LINE_SIZE - len(desc)) // 2)
    print(Style.DIM, padding + desc, Style.RESET_ALL)

    print('-' * LINE_SIZE)


def debug_mode(level):
    levels = ['', 'WARN', 'INFO', 'DEBUG']

    text = Fore.RED + ' ' + Icons.SOUND + ' '
    text += 'LOG LEVEL = %s' % levels[level]
    text += Fore.RESET

    padding = ' ' * ((LINE_SIZE - len(text)) // 2)
    print(padding + text)

    print('-' * LINE_SIZE)


def cancel_method():
    print()
    print(Icons.RIGHT_ARROW, 'Press', Fore.MAGENTA,
          'Ctrl + C', Fore.RESET, 'to exit')
    print()


def url_not_recognized(choice_list):
    print()
    print('-' * LINE_SIZE)
    print('Sorry! I do not recognize this website yet.')
    print('My domain is limited to these sites only:')
    for url in sorted(choice_list.keys()):
        print(Fore.LIGHTGREEN_EX, Icons.RIGHT_ARROW, url, Fore.RESET)

    print()
    print('-' * LINE_SIZE)
    print('Request developers to add your site at:')
    print(Fore.CYAN, Icons.LINK,
          'https://github.com/dipu-bd/lightnovel-crawler/issues', Fore.RESET)
    print()
