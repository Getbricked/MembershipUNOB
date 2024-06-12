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
        "users": config.getboolean("DataImport", "users"),
        "groups": config.getboolean("DataImport", "groups"),
        "memberships": config.getboolean("DataImport", "memberships"),
    }

    return config_values


def default_config():
    config = configparser.ConfigParser()

    config["Webscraping"] = {"get_data": "True", "extract_data": "True"}
    config["DataImport"] = {
        "users": "True",
        "groups": "True",
        "memberships": "True",
    }

    # Write the configuration to a file
    with open("config.ini", "w") as configfile:
        config.write(configfile)


def validate_config():
    default_values = {
        "Webscraping": {"get_data": True, "extract_data": True},
        "DataImport": {
            "users": True,
            "groups": True,
            "memberships": True,
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


def config_check_web(config):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if config:
                print("Executing " + func.__name__ + "...")
                return func(*args, **kwargs)
            else:
                print("Skipping " + func.__name__ + "...")
                return None

        return wrapper

    return decorator


def config_check_import(key):
    def decorator(func):
        async def wrapper(config, data, db_writer, gql_func):
            if config.get(key, False):
                print(f"Executing {key} import...")
                await func(data[key], db_writer, gql_func)
            else:
                print(f"Skipping {key} import...")

        return wrapper

    return decorator
