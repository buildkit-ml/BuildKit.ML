import os
from typing import Dict
from spython.main import Client

class Builder:
    def __init__(self) -> None:
        self.client = Client
    
    def build(self, config: Dict) -> None:
        build_folder = os.path.abspath(os.path.dirname(config['recipe']))
        print(build_folder)
        self.client.build(
            recipe=config['recipe'],
            image=config['target'],
            sudo=False,
            build_folder=build_folder,
            options=["--fakeroot"],
        )