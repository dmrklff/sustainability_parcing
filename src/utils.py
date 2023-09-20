import logging
from pathlib import Path
from typing import Dict, Any
import yaml

LOGGER = logging.getLogger()


def get_yaml_config(path: Path) -> Dict[str, Any]:
    """Get anything what was in yaml."""
    config = None
    if not path.exists():
        LOGGER.warning(f'Config file {path} does not exist.')
    else:
        with open(str(path)) as conf_file:
            config = yaml.load(conf_file, Loader=yaml.Loader)
    return {} if config is None else config
