import configparser

CONFIG_PATHS = ["./practicer_config.ini"]


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATHS)
    return config


def _write_defaul_config():
    config = configparser.ConfigParser()
    config["TEMPLATE"] = {"DEFAULT": "./templates/default.clip"}
    config["EXERCISES"] = {"PATH": "./exercises"}
    config["WORK"] = {"PATH": "Z:/zeichnungen"}
    config["REFERENCES"] = {"PATH": "Z:/referenzen/Fashion"}


    with open(CONFIG_PATHS[0], "w") as configfile:
        config.write(configfile)
