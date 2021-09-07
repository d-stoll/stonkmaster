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
        'yfinance>=0.1.63',
        'discord.py>=1.7.3',
        'holidays>=0.11.2',
        'plotly>=5.3.1',
        'pandas>=1.3.2',
        'pandas-datareader>=0.10.0',
        'secedgar>=0.3.3'
    ],

    setup_requires=[
        'pytest-runner>=5.3.1',
        'flake8>=3.9.2'
    ],

    tests_require=[
        'pytest>=6.2.5',
        'dpytest>=0.5.3'
    ],

    entry_points='''
        [console_scripts]
        stonkmaster=stonkmaster.main:main
    ''',
)