import re

from bs4 import BeautifulSoup

from classificator.utils.constants import BASE_PATH
from classificator import DBEngine


class Parser:
    def __init__(self, path: str) -> None:
        self.path = f'{BASE_PATH}/{path}'
        self.content = None
        self.soup = None
        self.content_body = None
        self.content_published_time = None
        self.content_title = None
        self.content_description = None

    def __enter__(self):
        with open(self.path) as f:
            self.content = f.read()

        if not self.content:
            raise BaseException('No content.')

        return self._parse()

    def __exit__(self, *args):
        pass

    def _parse(self) -> 'Parser':
        self.soup = BeautifulSoup(self.content, 'lxml')

        self.content_body = re.sub(r'[^a-zA-Z][ +]', '', ' '.join([p.text for p in self.soup.find_all('p')]))
        self.content_published_time = self.soup.find('meta', property='article:published_time')['content']
        self.content_description = self.soup.find('meta', property='og:description')['content']
        self.content_title = self.soup.find('meta', property='og:title')['content']
        return self

    def write_to_db(self):
        with DBEngine() as db_engine:
            db_engine.insert(table='datasets', data=[self.data])

    @property
    def data(self):
        return {
            'body': self.content_body,
            'title': self.content_title,
            'description': self.content_description,
            'published_time': self.content_published_time,
        }
