from .crawler import Crawler
from .boxnovel import BoxNovelCrawler
from .idqidian import IdqidianCrawler
from .lnindo import LnindoCrawler
from .lnmtl import LNMTLCrawler
from .novelplanet import NovelPlanetCrawler
from .readln import ReadLightNovelCrawler
from .webnovel import WebnovelCrawler
from .wuxiaworld import WuxiaWorldCrawler
from .wuxiac import WuxiaCoCrawler
from .wuxiaonline import WuxiaOnlineCrawler

__all__ = [
    Crawler.__name__,
    BoxNovelCrawler.__name__,
    IdqidianCrawler.__name__,
    LnindoCrawler.__name__,
    LNMTLCrawler.__name__,
    NovelPlanetCrawler.__name__,
    ReadLightNovelCrawler.__name__,
    WebnovelCrawler.__name__,
    WuxiaWorldCrawler.__name__,
    WuxiaCoCrawler.__name__,
    WuxiaOnlineCrawler.__name__
]

spiders = {
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
