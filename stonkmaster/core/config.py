import argparse
import configparser


def get_config(args: list[str]) -> configparser.ConfigParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path of configuration file.", default="/opt/stonkmaster/default.ini")
    args = parser.parse_args(args)

    config = configparser.ConfigParser()
    config.read(args.config)

    return config
