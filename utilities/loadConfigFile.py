import yaml

def loadConfigFile():
    """
    This function parses and extract data from the YAML configuration file 

    :return: Defined variables in the configuration file
    :rtype: Dict
    """
    
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


