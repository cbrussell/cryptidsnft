from os import error
import os.path
import random
from typing import List, Dict, Union
import json
from dataclasses import dataclass
import hashlib

class Frames:
    def __init(self, tail: list, left_back_leg: list):
        self.tail=tail
        self.left_back_leg = left_back_leg

class Manifest:
    def __init__(self, manifest):
        self.manifest=manifest

    def attribute(self, attr:str):
        return [x for x in self.manifest if x["attribute"] == attr][0]

def to_hash(data):
    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()

def chance(rarity):
    return random.random() < rarity

# input attribute, get frames and dict of attribute: trait pair
# if rarity <1, possibility to get empty list returned (no trait chosen)
# will be used for tail, ears, horns, eyes
def main():
    hashlist = []
    collection = 0
    collection_size = 8888
    attempts = 0
    unique_dna_tolerance = 20

    while attempts < unique_dna_tolerance:

        dna = get_dna()
        hashed_dna = to_hash(dna)

        # stop when collection is fulfilled
        if len(hashlist) == collection_size:

            print("Collection complete.")
            break
        if hashed_dna not in hashlist:
            hashlist.append(hashed_dna)
            collection += 1
        else:
            attempts+=1
            print("Duplicate DNA found...")
    
    print(len(hashlist))
    print




    # print(f"failed 200 times, final hashlist is {hashlist}")

        # if hash in hashlist:
        #     print(hashlist)
        #     break
        # else:
        #     hashlist.append(hash(dna))


def get_dna():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    manifest = Manifest(json.load(open(f'{dir_path}/manifest.json')))
    data = {}
    # only use first returned variable with [0]
    background = get_trait(manifest, "0_background")[0]
    data.update(background)

    tail = get_trait(manifest, "1_tail")[0]
    data.update(tail)

    leftbackleg, backanimalleg = get_trait(manifest, "2_leftbackleg")
    data.update(leftbackleg)

    leftfrontleg, frontanimalleg = get_trait(manifest, "3_leftfrontleg")
    data.update(leftfrontleg)

    back = get_trait(manifest, "4_back")[0]
    data.update(back)

    torsobase, torsotype = get_trait(manifest, "5a_torsobase")
    data.update(torsobase)

    # torso accent needs to relate to torso base, input type
    torsoaccent = get_trait_related(manifest, "5b_torsoaccent", torsotype)[0]
    data.update(torsoaccent)

    torsopattern = get_trait_related(manifest, "5b_torsoaccent", torsotype)[0]

    return data




def get_trait(manifest: Manifest, attribute: str) -> Dict:
    attrib = manifest.attribute(attribute)
    categories = attrib["categories"]
    if chance(attrib["rarity"]):
        category = random.choices(population = categories, weights = [x["weight"] for x in categories], k=1)[0]
        traits = category["traits"]
        trait = random.choices(population = traits, weights = [x["weight"] for x in traits], k=1)[0]
    else:
        return {}, ''
    data = {}
    data[attribute]=trait['trait']
    return data, category['category']


# based on previous trait, only look at related subcategories for random choice
# weigh category groups to themselves as 
def get_trait_related(manifest: Manifest, attribute: str, type: str) -> Dict:
    attrib = manifest.attribute(attribute)
    categories = attrib["categories"]
    if chance(attrib["rarity"]):
        category = random.choices(population = [x for x in categories if x["category"] == type], weights = [x["weight"] for x in categories if x["category"] == type], k=1)[0]
        traits = category["traits"]
        trait = random.choices(population = traits, weights = [x["weight"] for x in traits], k=1)[0]
    else:
        return {}, ''
    data = {}
    data[attribute]=trait['trait']
    return data, category['category']


if __name__ == "__main__":
    main()
    # get_dna()
