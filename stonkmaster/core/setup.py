import configparser
import os
import shutil


def create_data_dir(config: configparser.ConfigParser):
    if not os.path.isdir(config['stonkmaster']['TmpFolder']):
        os.makedirs(config['stonkmaster']['TmpFolder'])


def delete_data_dir(config: configparser.ConfigParser):
    if os.path.isdir(config['stonkmaster']['TmpFolder']):
        shutil.rmtree(config['stonkmaster']['TmpFolder'], ignore_errors=True)
