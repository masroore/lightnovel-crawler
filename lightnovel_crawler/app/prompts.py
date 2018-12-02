import sys
from PyInquirer import prompt

from .arguments import get_args


def get_novel_url():
    url = get_args().novel_page
    if url and url.startswith('http'):
        return url
    # end if

    answer = prompt([
        {
            'type': 'input',
            'name': 'novel',
            'message': 'What is the url of novel page?',
            'validate': lambda val: 'Url should be not be empty'
            if len(val) == 0 else True,
        },
    ])

    return answer['novel'].strip()
# end def


def force_replace_old():
    if len(sys.argv) > 1:
        return get_args().force
    # end if
    answer = prompt([
        {
            'type': 'confirm',
            'name': 'force',
            'message': 'Detected existing folder. Replace it?',
            'default': False,
        },
    ])
    return answer['force']
# end def
