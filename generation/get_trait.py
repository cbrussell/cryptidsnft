from os import error
import os.path
import random
import json
from typing import Union
from dataclasses import dataclass
import hashlib
from shutil import copy
from PIL import Image

@dataclass
class Frames:
    background_frames: list
    tail_frames: list
    leftbackleg_frames: list
    leftfrontleg_frames: list
    back_frames: list
    torsobase_frames: list
    torsoaccent_frames: list
    torsopattern_frames: list
    neckbase_frames: list
    fur_frames: list



class Manifest:
    def __init__(self, manifest):
        self.manifest=manifest

    def attribute(self, attr:str):
        return [x for x in self.manifest if x["attribute"] == attr][0]

def to_hash(data):
    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()

def chance(rarity):
    return random.random() < rarity


def main():
    hashlist = []
    edition = 0
    collection_size = 10
    attempts = 0
    unique_dna_tolerance = 1000
    dir_path = os.path.dirname(os.path.realpath(__file__))
    while attempts < unique_dna_tolerance:

        images, dna  = get_dna()
        hashed_dna = to_hash(dna)
        
        # stop when collection size is fulfilled
        if len(hashlist) == collection_size:

            print("Collection complete.")
            break

        if hashed_dna not in hashlist:
            hashlist.append(hashed_dna)
            edition += 1
            os.makedirs(f"{dir_path}/output/raw/{str(edition)}", exist_ok=True)
            os.makedirs(f"{dir_path}/output/metadata", exist_ok=True)
            with open(f"{dir_path}/output/metadata/{str(edition)}.json", "w") as f:
                json.dump(dna, f, indent=4)

            combine_attributes(images, str(edition))
            print(f"Done {edition}")

            
        else:
            attempts+=1
            print("Duplicate DNA found...")
    collection_total = len(hashlist)
    print(f'{collection_total} of {collection_size} generated.')



def get_dna() -> Union[Frames, dict]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    manifest = Manifest(json.load(open(f'{dir_path}/manifest.json')))
    data = {}
    # only use first returned variable with [0]
    background, background_frames = get_trait(manifest, "0_background")[0:3:2]
    data.update(background)

    tail, tail_frames = get_trait(manifest, "1_tail")[0:3:2]
    data.update(tail)


    leftbackleg, backanimalleg, leftbackleg_frames = get_trait(manifest, "2_leftbackleg")
    data.update(leftbackleg)

    leftfrontleg, frontanimalleg, leftfrontleg_frames  = get_trait(manifest, "3_leftfrontleg")
    data.update(leftfrontleg)

    back, back_frames = get_trait(manifest, "4_back")[0:3:2]
    data.update(back)

    torsobase, torsotype, torsobase_frames = get_trait(manifest, "5a_torsobase")
    data.update(torsobase)

    # torso accent needs to relate to torso base, input type
    torsoaccent, torsoaccent_frames = get_trait_related(manifest, "5b_torsoaccent", torsotype)[0:3:2]
    data.update(torsoaccent)

    torsopattern, torsopattern_frames = get_trait_related(manifest, "5c_torsopattern", torsotype)[0:3:2]
    data.update(torsopattern)

    neckbase, neckbase_frames = get_trait(manifest, "6a_neckbase")[0:3:2]
    data.update(neckbase)

    fur, fur_frames = get_trait(manifest, "7_fur")[0:3:2]
    data.update(fur) 

    return Frames(background_frames, tail_frames, leftbackleg_frames, leftfrontleg_frames, back_frames, torsobase_frames, torsoaccent_frames, torsopattern_frames, neckbase_frames, fur_frames), data


def get_trait(manifest: Manifest, attribute: str) -> Union[dict, str, list]:
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


# based on previous trait, only look at related subcategories for random choice
# weigh category groups to themselves as 
def get_trait_related(manifest: Manifest, attribute: str, type: str) -> Union[dict, str, list]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    attrib = manifest.attribute(attribute)
    categories = attrib["categories"]
    if chance(attrib["rarity"]):
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

def combine_attributes(frames: Frames, prefix: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for (n, background) in enumerate(frames.background_frames):
        print(background)
        print(n)
        frame = Image.open(background)

        if frames.tail_frames:
            print(frames.tail_frames[n])
            tail = Image.open(frames.tail_frames[n])
            frame.paste(tail, mask=tail)

        if frames.leftbackleg_frames:
            leftbackleg = Image.open(frames.leftbackleg_frames[n])
            frame.paste(leftbackleg, mask=leftbackleg)

        if frames.leftfrontleg_frames[n]:
            leftfrontleg = Image.open(frames.leftfrontleg_frames[n])
            frame.paste(leftfrontleg, mask=leftfrontleg)

        if frames.back_frames:
            back = Image.open(frames.back_frames[n])
            frame.paste(back, mask=back)
       
        if frames.torsobase_frames:
            torsobase = Image.open(frames.torsobase_frames[n])
            frame.paste(torsobase, mask=torsobase)

        if frames.torsoaccent_frames:
            torsoaccent = Image.open(frames.torsoaccent_frames[n])
            frame.paste(torsoaccent, mask=torsoaccent)

        if frames.torsopattern_frames:
            print("yes")
            print(frames.torsopattern_frames)
            torsopattern = Image.open(frames.torsopattern_frames[n])
            frame.paste(torsopattern, mask=torsopattern)

        if frames.neckbase_frames:
            neckbase = Image.open(frames.neckbase_frames[n])
            frame.paste(neckbase, mask=neckbase)

        if frames.fur_frames:
            fur= Image.open(frames.fur_frames[n])
            frame.paste(fur, mask=fur)
        print("almost there")

        frame.save(f"{dir_path}/output/raw/{prefix}/{prefix}_{n:05}.png")
        print(dir_path)

if __name__ == "__main__":
    main()
    # get_dna()
