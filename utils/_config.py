import configparser


def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read("config.ini")

    # Return a dictionary with the retrieved values
    config_values = {
        "get_data": config.getboolean("Webscraping", "get_data"),
        "extract_data": config.getboolean("Webscraping", "extract_data"),
        "import_user": config.getboolean("DataImport", "import_user"),
        "import_group": config.getboolean("DataImport", "import_group"),
        "import_membership": config.getboolean("DataImport", "import_membership"),
    }

    return config_values


def default_config():
    config = configparser.ConfigParser()

    config["Webscraping"] = {"get_data": "True", "extract_data": "True"}
    config["DataImport"] = {
        "import_user": "True",
        "import_group": "True",
        "import_membership": "True",
    }

    # Write the configuration to a file
    with open("config.ini", "w") as configfile:
        config.write(configfile)


def validate_config():
    default_values = {
        "Webscraping": {"get_data": True, "extract_data": True},
        "DataImport": {
            "import_user": True,
            "import_group": True,
            "import_membership": True,
        },
    }

    config = configparser.ConfigParser()
    config.read("config.ini")

    try:
        for section, keys in default_values.items():
            if section not in config:
                raise ValueError(f"Missing section: {section}")
            for key, default_value in keys.items():
                if key not in config[section]:
                    raise ValueError(f"Missing key: {key} in section: {section}")
                if config.get(section, key).lower() not in ["true", "false"]:
                    raise ValueError(
                        f"Invalid value for key: {key} in section: {section}"
                    )

        # If all values are valid, parse them as booleans
        config_values = {
            section: {key: config.getboolean(section, key) for key in keys}
            for section, keys in default_values.items()
        }

    except Exception as e:
        print(f"Exception caught: {e}")
        print("Rewriting config with default values.")
        default_config()
        config_values = default_values

    return config_values


config_web = validate_config()["Webscraping"]

config_data = validate_config()["DataImport"]
