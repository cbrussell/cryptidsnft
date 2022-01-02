import os.path
import random
from typing import List, Dict, Union
import json
from dataclasses import dataclass

class Frames:
    def __init(self, tail: list, left_back_leg: list):
        self.tail=tail
        self.left_back_leg = left_back_leg

class Manifest:
    def __init__(self, manifest):
        self.manifest=manifest

    def attribute(self, attr:str):
        return [x for x in self.manifest if x["attribute"] == attr][0]



def chance(rarity):
    return random.random() < rarity

# input attribute, get frames and dict of attribute: trait pair
# if rarity <1, possibility to get empty list returned (no trait chosen)
# will be used for tail, ears, horns, eyes



def get_dna():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    manifest = Manifest(json.load(open(f'{dir_path}/manifest.json')))

    data = {}

    background, type = get_trait(manifest, "0_background")
    data.update(background)
    # print(type)

    tail, type = get_trait(manifest, "1_tail")
    data.update(tail)
    # print(type)

    leftbackleg, animal = get_trait(manifest, "2_leftbackleg")
    data.update(leftbackleg)
    # print(animal)

    leftfrontleg, animal = get_trait(manifest, "3_leftfrontleg")
    data.update(leftfrontleg)
    # print(animal)

    back, type = get_trait(manifest, "4_back")
    data.update(back)
    # print(type)

    torsobase, type = get_trait(manifest, "5a_torsobase")
    data.update(torsobase)
    # print(type)

    torsoaccent, color = get_trait_related(manifest, "5b_torsoaccent", type)


    # print(torsoaccent)
    # print(color)
    data.update(torsoaccent)

    print(data)


def get_trait(manifest: Manifest, attribute: str) -> Dict:
    attrib = manifest.attribute(attribute)
    categories = attrib["categories"]
    # print(categories)
    if chance(attrib["rarity"]):
        category = random.choices(population = categories, weights = [x["weight"] for x in categories], k=1)[0]

        # print(category)
        traits = category["traits"]
        trait = random.choices(population = traits, weights = [x["weight"] for x in traits], k=1)[0]
    else:
        return {}, ''
    data = {}
    data[attribute]=trait['trait']
    return data, category['category']

def get_trait_related(manifest: Manifest, attribute: str, type: str) -> Dict:
    attrib = manifest.attribute(attribute)
    categories = attrib["categories"]
    # print(categories)
    if chance(attrib["rarity"]):
        category = random.choices(population = [x for x in categories if x["category"] == type], weights = [x["weight"] for x in categories if x["category"] == type], k=1)[0]

        # print(category)
        traits = category["traits"]
        trait = random.choices(population = traits, weights = [x["weight"] for x in traits], k=1)[0]
    else:
        return {}, ''
    data = {}
    data[attribute]=trait['trait']
    return data, category['category']

    # [x for x in categories if x["category"] == type][0]


if __name__ == "__main__":
    get_dna()
