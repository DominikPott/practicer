import configparser
import os
import pathlib

PACKAGE_DIR = pathlib.Path(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
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

    config["TEMPLATE"] = {"DEFAULT": PACKAGE_DIR / "templates/default.psd"}
    config["EXERCISES"] = {"PATH": PACKAGE_DIR / "exercises"}
    config["WORK"] = {"PATH": "Z:/zeichnungen"}
    config["REFERENCES"] = {"PATH": "Z:/referenzen/Fashion"}
    config["STATS"] = {"PATH": PACKAGE_DIR / "fs_exercise_stats"}

    with open(path, "w") as fp:
        config.write(fp)


if __name__ == '__main__':
    _write_default_config()
