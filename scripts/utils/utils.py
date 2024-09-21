import logging
import requests
from dataclasses import dataclass
from functools import cached_property

logger = logging.getLogger(__name__)

@dataclass
class SpotifyManager:
    client_id: str
    client_secret: str
    urls:dict

