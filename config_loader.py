import configparser

_CONFIG_PATHS = ["./practicer_config.ini"]


def read_config():
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATHS)
    return config


def _write_defaul_config():
    config = configpsarser.ConfigParser()
    config["TEMPLATE"] = {"DEFAULT": "./templates/default.clip"}
    config["EXERCISES"] = {"PATH": "./exercises"}
    config["WORK"] = {"PATH": "Z:/zeichnungen"}
    config["REFERENCES"] = {"PATH": "Z:/referenzen/Fashion"}
    config["STATS"] = {"PATH": "./fs_exercise_stats"}


    with open(_CONFIG_PATHS[0], "w") as configfile:
        config.write(configfile)
