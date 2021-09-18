import argparse
import configparser

import pkg_resources


def get_config(args: list[str]) -> configparser.ConfigParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path of configuration file.",
                        default=pkg_resources.resource_filename(__name__, "default.ini"))
    args = parser.parse_args(args)

    config = configparser.ConfigParser()
    config.read(args.config)

    return config
