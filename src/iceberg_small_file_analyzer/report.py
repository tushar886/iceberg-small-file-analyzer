# Author: Tushar Srivastava
import json
from dataclasses import asdict
from .models import TableProfile

def to_json(profile: TableProfile) -> str:
    return json.dumps(asdict(profile), indent=2)
