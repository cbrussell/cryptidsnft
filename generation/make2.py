
from dataclasses import dataclass
from typing import List, Dict
import json
import os
# from get_components2 import get
import random

@dataclass
class Frames:
    leftarm: List
    panels: List[List]
    rightarm: List
    space: List[List]
    base: List
    cockpit: List
    window: List

class Manifest:
    def __init__(self, manifest):
        self.manifest = manifest

    def attribute(self, attr: str):
        return [x for x in self.manifest if x["attribute"] == attr][0]

def get_attributes(manifest: Manifest) -> List[Frames, Dict]:

    dir_path = os.path.dirname(os.path.realpath(__file__))

    manifest = Manifest(json.load(open(f"{dir_path}/files_manifest.json")))
    # Get each of them according to manifest
    data = {}

    leftarm, d = get(manifest.attribute("left-arm"))

    data.update(d)

    return Frames(leftarm), data

def fetch_categories(manifest) -> List:
    # Get all categories
    categories = manifest["categories"]

    # If not multiple then pick one based on relative rarity.
    # However, if there are multiple available, then all categories are selected. The base chance will
    # be compounded by individual files.
    if not manifest["multiple"]:
        categories = random.choices(
            population=categories, weights=[x["rarity"] for x in categories], k=1
        )

    return categories
