import configparser
from abc import ABC


class BaseCommand(ABC):
    def __init__(self, config: configparser.ConfigParser):
        self.config = config
