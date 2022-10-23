import os
from typing import Dict
from loguru import logger
from spython.main import Client
from pySmartDL import SmartDL

class Builder:
    def __init__(self) -> None:
        self.client = Client

    def build(self, config: Dict) -> None:
        build_folder = os.path.abspath(os.path.dirname(config['recipe']))
        options = []
        if 'fakeroot' in config:
            if config['fakeroot']:
                options.append('--fakeroot')
        self.client.build(
            recipe=config['recipe'],
            image=config['target'],
            sudo=False,
            build_folder=build_folder,
            options=options,
        )
        if 'sign' in config:
            logger.info("Signing image with your pgp key")
            os.system(f"singularity sign {config['target']}")

    def download(self, config: Dict) -> None:
        logger.info(f"Downloading image from {config['pull']} to ./")
        obj = SmartDL(config['pull'], './')
        obj.start()
        file_name = obj.get_dest()
        os.rename(file_name, config['target'])