from os import environ
from pathlib import Path
import json

try:
    CONFIG_DIR = Path(environ['XDG_CONFIG_HOME'], __package__)
except KeyError:
    CONFIG_DIR = Path.home() / '.config' / __package__

CONFIG_FILE = CONFIG_DIR / 'config.json'

with open(CONFIG_FILE) as f:
    config = json.load(f)

TOKEN = config['token']
START_MESSAGE = config['start-message']
RESPONSE_CAPTION = config['response-caption']
FRAME_PATH = Path(config['frame-path'])

if not FRAME_PATH.is_absolute():
    FRAME_PATH = CONFIG_DIR / FRAME_PATH
