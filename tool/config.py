import json

from os.path import dirname


class Config:

    config = {}
    
    def __init__(self) -> None:

        config_path = f'{dirname(__file__)}/../config.json'
        with open(config_path, 'r') as config_file:
            config_dict = json.load(config_file)

        self.config = config_dict