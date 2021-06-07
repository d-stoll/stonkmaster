from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='stonkmaster',
    version='1.0.0',
    description='Discord bot for stonks',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/d-stoll/stonkmaster',
    license='Apache License 2.0',
    keywords='discord discord-bot stocks',

    packages=find_packages(exclude=['tests', 'tests.*']),

    python_requires='>=3.7, <4',
    install_requires=[
        'yfinance',
        'discord.py',
        'holidays',
        'plotly',
        'pandas'
    ],

    entry_points='''
        [console_scripts]
        stonkmaster=stonkmaster.main:main
    ''',
)