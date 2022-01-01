# get tail randomly, using bonus rarit

import os.path
import random
from typing import List
import json

class Manifest:
    def __init__(self, manifest):
        self.manifest=manifest

    def attribute(self, attr:str):
        return [x for x in self.manifest if x["attribute"] == attr][0]


def chance(rarity):
    return random.random() < rarity


def get_tail():
    # get file directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # establish manifest 
    manifest = Manifest(json.load(open(f'{dir_path}/1_tails.json')))
    
    # get json list for tails
    tails = manifest.attribute('tail')

    # get list of tail categories
    categories = tails["categories"]
    # use rarity of attribute to see if cryptid gets it 
    # 1 = Cryptid will have this trait 100% of the time
    # 0.5 = 50%
    # chance function will return bool
    if chance(tails["rarity"]):
        # pick from selection of categories, open list with [0]
        category = random.choices(population = categories, weights = [x["weight"] for x in categories], k=1)[0]

        # list of files in winner of above choice
        files = category["files"]
        # use same choice mechanism, pick winnin file
        file = random.choices(population = files, weights = [x["weight"] for x in files], k=1)
        
        print(file)
    else:
        return []

    return file

if __name__ == "__main__":
    get_tail()
