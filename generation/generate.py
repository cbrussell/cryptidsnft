from os import dup, error
import os.path
import random
import json
from typing import Union
from dataclasses import dataclass
import hashlib
from shutil import copy
from PIL import Image
import numpy as np
from multiprocessing import Process, Manager, Value
from datetime import datetime

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
    fur_frames: list
    headbase_frames: list
    neckbase_frames: list
    neckaccent_frames: list
    neckpattern_frames: list
    neckshadow_frames: list
    rightbackleg_frames: list
    rightfrontleg_frames: list
    ears_frames: list

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
    start_time = datetime.now()
    procs = 20
    n = 20
    increment = int(n / procs)
    count = int(n/procs)
    jobs = []
    start = 1
    stop = increment + 1

    with Manager() as manager:
        hashlist = manager.list()
        duplicates = manager.Value('duplicates', 0)
        for i in range(0, procs):
            process = Process(target=worker, args=(start, stop, count, hashlist, duplicates))
            start = stop
            stop += increment
            jobs.append(process)

        [j.start() for j in jobs]
        [j.join() for j in jobs]

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        collection_total = (len(hashlist))
        print(f'{collection_total} of {n} cryptids generated in {elapsed_time}. {duplicates.value} duplicates found.')

    return

def worker(start: int, stop: int, count: int, hashlist: list, duplicates: int):
    number = 0

    unique_dna_tolerance = 10000

    dir_path = os.path.dirname(os.path.realpath(__file__))

    while duplicates.value < unique_dna_tolerance:
        images, dna  = get_dna()
        hashed_dna = to_hash(dna)

        if number == count:
            break

        for edition in range(start, stop):
            if hashed_dna not in hashlist:
                hashlist.append(hashed_dna)
                number += 1
                print(edition)
                os.makedirs(f"{dir_path}/output/raw/{str(edition)}", exist_ok=True)
                os.makedirs(f"{dir_path}/output/metadata", exist_ok=True)
                with open(f"{dir_path}/output/metadata/{str(edition)}.json", "w") as f:
                    json.dump(dna, f, indent=4)
                combine_attributes(images, str(edition))
                print(f"Done {edition}")
            else:
                with duplicates.get_lock():
                    duplicates.value += 1
                print("Duplicate DNA found...")

    collection_total = len(hashlist)
    print(f'Complete!\nFor this job, {number} generated. Found {duplicates.value} duplicates.')

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

    fur, fur_frames = get_trait(manifest, "7_fur")[0:3:2]
    data.update(fur) 

    headbase, animal, headbase_frames = get_trait(manifest, "11a_headbase")
    data.update(headbase)

    # if fur, ignore neck DNA
    if fur:
        neckbase_frames = []
        neckaccent_frames = []
        neckpattern_frames = []
        neckshadow_frames = []
    else:
        neckbase, neckbase_frames = get_trait(manifest, "6a_neckbase")[0:3:2]
        data.update(neckbase)

        # if accent on torso, must be accent on neck
        # neckaccent rarity driven by torso accent
        if torsoaccent:
            neckaccent, neckaccent_frames = get_trait(manifest, "6b_neckaccent")[0:3:2]
            data.update(neckaccent)
        else:
            neckaccent_frames = []
        
        if torsopattern:
            neckpattern, neckpattern_frames = get_trait(manifest, "6c_neckpattern")[0:3:2]
            data.update(neckpattern)
        else:
            neckpattern_frames = []
        
        # no neckshadow on eagle
        if animal == 'eagle':
            neckshadow_frames = []
        else:
            neckshadow, neckshadow_frames = get_trait_related(manifest, "6d_neckshadow", animal)[0:3:2]
            data.update(neckshadow)

    rightbackleg, rightbackleg_frames = get_trait_related(manifest, "8_rightbackleg", backanimalleg)[0:3:2]
    data.update(rightbackleg)

    rightfrontleg, rightfrontleg_frames = get_trait_related(manifest, "9_rightfrontleg", frontanimalleg)[0:3:2]
    data.update(rightfrontleg)

    ears, ears_frames = get_trait(manifest, "10_ears")[0:3:2]
    data.update(ears)

    return Frames(background_frames
                , tail_frames
                , leftbackleg_frames
                , leftfrontleg_frames
                , back_frames
                , torsobase_frames
                , torsoaccent_frames
                , torsopattern_frames
                , fur_frames
                , headbase_frames
                , neckbase_frames
                , neckaccent_frames
                , neckpattern_frames
                , neckshadow_frames
                , rightbackleg_frames
                , rightfrontleg_frames
                , ears_frames

                ), data


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
    # random frame color backhround
    # R = random.randint(0,255)
    # G = random.randint(0,255)
    # B = random.randint(0,255)
    R = 255
    G = 255
    B = 255
    # R2 = random.randint(0,255)
    # G2 = random.randint(0,255)
    # B2 = random.randint(0,255)
    
    # array = get_gradient_3d(1100, 1100, (R2, G2, B2), (R, G, B), (True, False, False))

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # for (n, background) in enumerate(frames.background_frames):
    for n in range(72):

        # use this is background color
        # frame = Image.open(background)

        frame = Image.new('RGB', (1100, 1100), (R, G, B))

        # frame = Image.fromarray(np.uint8(array))

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
            torsopattern = Image.open(frames.torsopattern_frames[n])
            frame.paste(torsopattern, mask=torsopattern)

        if frames.neckbase_frames:
            neckbase = Image.open(frames.neckbase_frames[n])
            frame.paste(neckbase, mask=neckbase)
        
        if frames.neckaccent_frames:
            neckaccent = Image.open(frames.neckaccent_frames[n])
            frame.paste(neckaccent, mask=neckaccent)

        if frames.neckpattern_frames:
            neckpattern = Image.open(frames.neckpattern_frames[n])
            frame.paste(neckpattern, mask=neckpattern)
        
        if frames.neckshadow_frames:
            neckshadow = Image.open(frames.neckshadow_frames[n])
            frame.paste(neckshadow, mask=neckshadow)

        if frames.fur_frames:
            fur = Image.open(frames.fur_frames[n])
            frame.paste(fur, mask=fur)

        if frames.rightbackleg_frames:
            rightbackleg = Image.open(frames.rightbackleg_frames[n])
            frame.paste(rightbackleg, mask=rightbackleg)
        
        if frames.rightfrontleg_frames:
            rightfrontleg = Image.open(frames.rightfrontleg_frames[n])
            frame.paste(rightfrontleg, mask=rightfrontleg)

        if frames.ears_frames:
            ears = Image.open(frames.ears_frames[n])
            frame.paste(ears, mask=ears)

        if frames.headbase_frames:
            headbase = Image.open(frames.headbase_frames[n])
            frame.paste(headbase, mask=headbase)

        print("Almost there...")

        frame.save(f"{dir_path}/output/raw/{prefix}/{prefix}_{n:03}.png")
        print(dir_path)


def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T
def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float)
    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)
    return result

if __name__ == "__main__":
    main()

