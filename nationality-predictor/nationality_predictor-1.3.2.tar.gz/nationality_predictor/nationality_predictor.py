import requests
from dataclasses import dataclass, field

@dataclass
class Predictor:
    name: str
    __url: str = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        if self.name != "":
            self.__url = f"https://api.nationalize.io?name={self.name}"
        else:
            raise ValueError("Name is not defined.")

    def predict(self):
        req = requests.get(self.__url)
        res = req.json()

        return res