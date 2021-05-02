import configparser
import os
import pathlib

PACKAGE_DIR = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
_CONFIG_PATHS = [PACKAGE_DIR / "config.cfg"]


def load():
    for path in _CONFIG_PATHS:
        if not os.path.exists(path):
            _write_default_config(path)
    return _read_config()


def _read_config():
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATHS)
    return config


def _write_default_config(path):
    config = configparser.ConfigParser()
    config["TEMPLATE"] = {"DEFAULT": PACKAGE_DIR / "resources/templates/default.psd"}
    config["EXERCISES"] = {"PATH": PACKAGE_DIR / "resources/exercises"}
    config["WORK"] = {"PATH": PACKAGE_DIR / "drawings"}
    config["STATS"] = {"PATH": PACKAGE_DIR / "fs_exercise_stats"}

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        config.write(fp)


if __name__ == '__main__':
    _write_default_config()
