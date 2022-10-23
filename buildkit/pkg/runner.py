import os
from typing import Dict
from loguru import logger
import requests
from spython.main import Client


class Runner:
    def __init__(self):
        self.client = Client
        self.apps = None

    def run_command(self, config: Dict, command: str, image_path=None):
        build_folder = os.path.abspath(os.path.dirname(config['recipe']))
        bind = []
        for key, value in config['bind'].items():
            bind.append(f"{value}:{key}")
        if image_path is None:
            self.client.load(os.path.join(build_folder, config['target']))
        else:
            self.client.load(os.path.join(image_path, config['target']))
        options = ['--pwd', '/app']
        
        if 'nvidia' in config:
            if config['nvidia']:
                options.append('--nv')
        if 'env' in config:
            options.append(f"--env-file {config['env']}")
        for line in self.client.execute(
            config['scripts'][command].split(" "),
            bind=bind,
            options=options,
            stream=True,
        ):
            print(line, end='')

    def run_pipeline(self, config: Dict, image_path=None, webhook=""):
        if webhook != "":
            # update status to be running
            res = requests.post(webhook, json={
                "type": "general",
                "status": "running",
            })
        for command in config['pipeline']:
           self.run_command(config, command, image_path)
        if webhook != "":
            # find results and push to toma
            res = requests.post(webhook, json={
                "type": "general",
                "status": "finished",
                "returned_payload": {
                    "files": os.listdir("results/")
                },
            })
