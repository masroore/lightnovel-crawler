# Novel Crawler

[![Python version](https://img.shields.io/pypi/pyversions/lightnovel-crawler.svg)](https://pypi.org/project/lightnovel-crawler)
[![PyPI version](https://img.shields.io/pypi/v/lightnovel-crawler.svg)](https://pypi.org/project/lightnovel-crawler)
[![GitHub issues](https://img.shields.io/github/issues/dipu-bd/lightnovel-crawler.svg)](https://github.com/dipu-bd/lightnovel-crawler/issues)
[![SayThanks.io](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/dipu-bd)
<!-- [![PyPI - Format](https://img.shields.io/pypi/format/lightnovel-crawler.svg)](https://pypi.org/project/lightnovel-crawler) -->
<!-- [![PyPI - Status](https://img.shields.io/pypi/status/lightnovel-crawler.svg)](https://pypi.org/project/lightnovel-crawler) -->
<!-- [![GitHub contributors](https://img.shields.io/github/contributors/dipu-bd/lightnovel-crawler.svg)](https://github.com/dipu-bd/lightnovel-crawler) -->
<!-- [![GitHub pull requests](https://img.shields.io/github/issues-pr/dipu-bd/lightnovel-crawler.svg)](https://github.com/dipu-bd/lightnovel-crawler/pulls) -->
<!-- [![GitHub closed issues](https://img.shields.io/github/issues-closed/dipu-bd/lightnovel-crawler.svg)](https://github.com/dipu-bd/lightnovel-crawler/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aclosed+) -->
<!-- [![GitHub](https://img.shields.io/github/license/dipu-bd/lightnovel-crawler.svg)](https://github.com/dipu-bd/lightnovel-crawler/blob/master/VERSION) -->

Crawls light novels and make html, text, epub and mobi

## Tutorial

```bash
$ lightnovel-crawler

# Or, a shortcut:
$ lncrawl
```

To view list of available options:

```bash
$ lncrawl -h
```

> There is a verbose mode for extended logging: `lncrawl -lll`

### Available websites

The list of crawable websites are given below:

- https://lnmtl.com
- https://www.webnovel.com
- https://wuxiaworld.online
- https://www.wuxiaworld.com
- https://www.wuxiaworld.co
- https://boxnovel.com
- https://www.readlightnovel.org
- https://novelplanet.com
- https://lnindo.org
- https://www.idqidian.us

## Adding new source

- Use the [`_sample.py`](https://github.com/masroore/novel_crawler/blob/master/lightnovel_crawler/_sample.py) as blueprint.
- Add your crawler to [`__init__.py`](https://github.com/masroore/novel_crawler/blob/master/lightnovel_crawler/__init__.py).

That's all!
