import numpy as np
import yaml
from functools import partial
from pathlib import Path
from chaotic_encrypter.chaos import henon, ikeda, lorenz, logistic, tinkerbell


class ChaosKey:

    @staticmethod
    def __henon_init():
        return {
            "map": "henon",
            'primer': int(np.random.randint(1, 1000, 1)),
            "params": [1.4, 0.3],
            "v0": np.random.uniform(-0.1, 0.1, 2).tolist()
        }

    @staticmethod
    def __lorenz_init():
        return {
            "map": "lorenz",
            'primer': int(np.random.randint(1, 1000, 1)),
            "params": [10, 28, 8 / 3],
            "v0": np.random.random(3).tolist()
        }

    @staticmethod
    def __logistic_init():
        return {
            "map": "logistic",
            'primer': int(np.random.randint(1, 1000, 1)),
            "params": [4],
            "v0": np.random.random(1).tolist()
        }

    @staticmethod
    def __ikeda_init():
        return {
            "map": "ikeda",
            'primer': int(np.random.randint(1, 1000, 1)),
            "params": [0.9],
            "v0": np.random.random(2).tolist()
        }
    
    def __call__(self, key_name: str):
        chaos_key = self.__get_chaos_key(Path.home().joinpath(".chaos-encrypt", key_name).with_suffix(".yaml"))
        chaos_maps = dict()
        for k, v in chaos_key.items():
            chaos_maps[k] = {
                "dim": len(v["v0"]),
                "primer": v["primer"],
                "func": partial(self.__get_chaotic_map(v["map"]), v["v0"], v["params"])
            }
        return chaos_maps

    def __get_chaos_key(self, key_path: Path):
        """
        The __get_chaos_key function is used to generate a random seed for the chaos functions.
        The keypath argument is a pathlib Path object that points to where the file should be saved.
        If it does not exist, then it will create one with random values and save it there. If it does exist, then
        it will load those values from that file and return them as a dictionary.

        :param keypath: Path: Specify the path to the key file
        :return: A dictionary of the form:
        :doc-author: Trelent
        """
        if not key_path.exists():
            return self.__init_key(key_path)
        with key_path.open('r') as reader:
            return yaml.safe_load(reader.read())

    def __init_key(self, key_path: Path):
        key_path.parent.mkdir(parents=True, exist_ok=True)
        chaos_key = {
            'henon': self.__henon_init(),
            'ikeda': self.__ikeda_init(),
            'lorenz': self.__lorenz_init(),
            'logistic': self.__logistic_init(),
        }
        with key_path.open('w') as writer:
            yaml.dump(chaos_key, writer)
        return chaos_key

    @staticmethod
    def __get_chaotic_map(map_name):
        if map_name == "henon":
            return henon
        elif map_name == "ikeda":
            return ikeda
        elif map_name == "lorenz":
            return lorenz
        elif map_name == "logistic":
            return logistic
        elif map_name == "tinkerbell":
            return tinkerbell
    