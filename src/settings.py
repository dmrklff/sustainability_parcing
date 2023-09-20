import os
from pathlib import Path

from utils import get_yaml_config

ROOT_PATH = Path(__file__).parents[1]
SRC_PATH = ROOT_PATH / "src"
INPUT_DATA_PATH = ROOT_PATH / "data" / "input_data"
OUTPUT_DATA_PATH = ROOT_PATH / "data" / "output_data"
DEFAULT_CONFIG_PATH = ROOT_PATH / "config.yaml"

config = get_yaml_config(DEFAULT_CONFIG_PATH)
OPENAI_TOKEN = os.environ.get("OPENAI_TOKEN", default=config.get("OPENAI_TOKEN"))
MODEL_NAME = os.environ.get("MODEL_NAME", default=config.get("MODEL_NAME"))
ARTICLE_NUMS = os.environ.get("ARTICLE_NUMS", default=config.get("ARTICLE_NUMS"))
