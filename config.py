import yaml
from yaml import Loader
import os
class Config():
    def __init__(self):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        yaml_file = os.path.join(self.current_path, 'config.yaml')

        config = self.load_configs(yaml_file)
        self.url = config['url']
        self.secret_key = config['secret_key']
        self.public_key = config['public_key']
        self.header_key = config['header_key']
        self.gmail_username = config['gmail_username']
        self.gmail_password = config['gmail_password']
        self.email_recipients = config['email_recipients']

    def load_configs(self, yaml_file):
        return yaml.load(open(yaml_file),Loader=Loader)


