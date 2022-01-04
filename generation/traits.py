import os
import random
from typing import Union

class TraitManifest:
    def __init__(self, manifest):
        self.manifest=manifest

    def attribute(self, attr:str):
        return [x for x in self.manifest if x["attribute"] == attr][0]
    
class ColorManifest:
    def __init__(self, manifest):
        self.manifest = manifest

    def get(self):
        color = random.choices(population=self.manifest, weights=[x["weight"] for x in self.manifest], k=1)[0]
        color = color["color"]
        return color

def chance(rarity):
    return random.random() < rarity

def get_trait(manifest: TraitManifest, attribute: str) -> Union[dict, str, list]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    attrib = manifest.attribute(attribute)
    categories = attrib["categories"]
    if chance(attrib["rarity"]):
        category = random.choices(population = categories, weights = [x["weight"] for x in categories], k=1)[0]
        traits = category["traits"]
        trait = random.choices(population = traits, weights = [x["weight"] for x in traits], k=1)[0]
    else:
        return {}, '', []
    data = {}
    data[attribute]=trait['trait']
    name = trait['trait']
    images = []
    for i in range(1, 73):
        file_name = f"{dir_path}/RENDERS/{attribute}/{name}/{name}_{i:03}.png"
        images.append(file_name)
    return data, category['category'], images

def get_trait_related(manifest: TraitManifest, attribute: str, type: str) -> Union[dict, str, list]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    attrib = manifest.attribute(attribute)
    categories = attrib["categories"]
    if chance(attrib["rarity"]):
        if [x["weight"] for x in categories if x["category"] == type][0] == 0:
            print(f'No weights set for {attribute}/{type}')
            return {}, '', []
        else:

            category = random.choices(population = [x for x in categories if x["category"] == type], weights = [x["weight"] for x in categories if x["category"] == type], k=1)[0]
            traits = category["traits"]
            trait = random.choices(population = traits, weights = [x["weight"] for x in traits], k=1)[0]
    else:
        return {}, '', []
    data = {}
    data[attribute]=trait['trait']
    name = trait['trait']
    images = []
    for i in range(1, 73):
        file_name = f"{dir_path}/RENDERS/{attribute}/{name}/{name}_{i:03}.png"
        images.append(file_name)
    return data, category['category'], images

