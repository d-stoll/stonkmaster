import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='stonkmaster',
    version='1.0.1',
    author='Daniel Stoll',
    author_email='danielsimon.stoll2@gmail.com',
    description='Simple bot to monitor stocks, options and cryptos.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/d-stoll/stonkmaster',
    project_urls={
        "Bug Tracker": "https://github.com/d-stoll/stonkmaster/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],

    license='Apache License 2.0',
    keywords='discord discord-bot stocks',

    packages=find_packages(exclude=['tests', 'tests.*']),

    include_package_data=True,
    data_files=[("config", ["default.ini"])],

    python_requires='>=3.8, <4',
    install_requires=[
        'aiohttp==3.7.4.post0',
        'yfinance>=0.1.63',
        'discord.py>=1.7.3',
        'holidays>=0.11.2',
        'plotly>=5.3.1',
        'pandas>=1.3.2',
        'secedgar==0.4.0a2',
        'kaleido==0.2.1'
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
