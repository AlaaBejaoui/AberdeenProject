import yaml

def loadConfigFile():
    """load configuration file
    """
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


