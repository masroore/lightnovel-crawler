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
