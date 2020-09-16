import yaml

def loadConfigFile():
    """
    This function parses and extracts data from the yaml configuration file 

    :return: Variables defined by the user in the configuration file
    :rtype: Dictionary
    """
    
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


