import configparser


def get_text(key: str, config: configparser) -> str:
    language = config["stonkmaster"]["language"]
    return config[f"messages.{language}"][key]
