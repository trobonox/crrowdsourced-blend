import json

from types import SimpleNamespace


def load(filename=None, dev=False):
    if filename is None:
        filename = "config.dev" if dev else "config"

    try:
        with open(f"{filename}.json", encoding="utf8") as data:
            return data.read()

    except FileNotFoundError:
        raise FileNotFoundError("Config file was not found.")


def config():
    raw_json_data = load()

    # Parse JSON into an object with attributes corresponding to dict keys.
    return json.loads(raw_json_data, object_hook=lambda d: SimpleNamespace(**d))
