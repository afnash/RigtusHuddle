from typing import List, Dict
import json

def load_linkedin_comments(path: str) -> List[Dict]:
    """
    Loads LinkedIn comments JSON file.
    """
    with open(path, "r") as f:
        return json.load(f)
