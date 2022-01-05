import json
import hashlib
from dataclasses import dataclass
from typing import Union
from traits import TraitManifest, ColorManifest, get_trait, get_trait_category, get_trait_category_color, get_trait_color

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
    headaccent_frames: list
    headpattern_frames: list
    mouth_frames: list
    neckbase_frames: list
    neckaccent_frames: list
    neckpattern_frames: list
    neckshadow_frames: list
    rightbackleg_frames: list
    rightfrontleg_frames: list
    ears_frames: list
    horns_frames: list
    eyes_frames: list

def to_hash(data):
    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()

def get_dna(trait_manifest: TraitManifest, color_manifest: ColorManifest) -> Union[Frames, dict]:
    data = {}

    color = color_manifest.get()
    data["base_color"] = color

    # get background, independet trait
    background, background_frames = get_trait(trait_manifest, "0_background")[0:4:3]
    data.update(background)

    # force brush tail to color of base fur
    tail, tail_frames = get_trait(trait_manifest, "1_tail")[0:4:3]
    data.update(tail)

    leftbackleg, backanimalleg, leftbackleg_color, leftbackleg_frames = get_trait(trait_manifest, "2_leftbackleg")
    data.update(leftbackleg)

    leftfrontleg, frontanimalleg, leftfrontleg_color, leftfrontleg_frames  = get_trait(trait_manifest, "3_leftfrontleg")
    data.update(leftfrontleg)

    back, back_frames = get_trait(trait_manifest, "4_back")[0:4:3]
    data.update(back)

    torsobase, torsotype, torsobase_color, torsobase_frames = get_trait(trait_manifest, "5a_torsobase")
    data.update(torsobase)

    # torso accent needs to relate to torso base, input type
    torsoaccent, torsoaccent_category, torsoaccent_color, torsoaccent_frames = get_trait_category(trait_manifest, "5b_torsoaccent", torsotype)
    data.update(torsoaccent)

    torsopattern, torsopattern_category, torsopattern_color, torsopattern_frames = get_trait_category(trait_manifest, "5c_torsopattern", torsotype)
    data.update(torsopattern)

    fur, fur_frames = get_trait(trait_manifest, "7_fur")[0:4:3]
    data.update(fur) 

    headbase, animal, animalcolor, headbase_frames = get_trait(trait_manifest, "11a_headbase")
    data.update(headbase)

    headaccent, headaccent_frames = get_trait_category(trait_manifest, "11b_headaccent", animal)[0:4:3]
    data.update(headaccent)

    headpattern, headpattern_frames = get_trait_category(trait_manifest, "11c_headpattern", animal)[0:4:3]
    data.update(headpattern)

    mouth, mouth_frames = get_trait_category(trait_manifest, "12_mouth", animal)[0:4:3]
    data.update(mouth)

    # if fur, ignore neck DNA
    if fur:
        neckbase_frames = []
        neckaccent_frames = []
        neckpattern_frames = []
        neckshadow_frames = []
    else:
        neckbase, neckbase_frames = get_trait(trait_manifest, "6a_neckbase")[0:4:3]
        data.update(neckbase)
        
        # if accent on torso, must be accent on neck
        # neckaccent rarity driven by torso accent
        # match accent type of neck to accent type of torso
        if torsoaccent:
            neckaccent, neckaccent_frames = get_trait_category(trait_manifest, "6b_neckaccent", torsoaccent_category)[0:4:3]
            data.update(neckaccent)
        else:
            neckaccent_frames = []
        

        if torsopattern:
            neckpattern, neckpattern_frames = get_trait_category(trait_manifest, "6c_neckpattern", torsopattern_category )[0:4:3]
            data.update(neckpattern)
        else:
            neckpattern_frames = []
        
        # no neckshadow on eagle
        if animal == 'eagle':
            neckshadow_frames = []
        else:
            neckshadow, neckshadow_frames = get_trait_category(trait_manifest, "6d_neckshadow", animal)[0:4:3]
            data.update(neckshadow)

    rightbackleg, rightbackleg_frames = get_trait_category(trait_manifest, "8_rightbackleg", backanimalleg)[0:4:3]
    data.update(rightbackleg)

    rightfrontleg, rightfrontleg_frames = get_trait_category(trait_manifest, "9_rightfrontleg", frontanimalleg)[0:4:3]
    data.update(rightfrontleg)

    ears, ears_frames = get_trait(trait_manifest, "10_ears")[0:4:3]
    data.update(ears)

    horns, horns_frames = get_trait(trait_manifest, "13_horns")[0:4:3]
    data.update(horns)

    eyes, eyes_frames = get_trait(trait_manifest, "14_eyes")[0:4:3]
    data.update(eyes)

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
                , headaccent_frames
                , headpattern_frames
                , mouth_frames
                , neckbase_frames
                , neckaccent_frames
                , neckpattern_frames
                , neckshadow_frames
                , rightbackleg_frames
                , rightfrontleg_frames
                , ears_frames
                , horns_frames
                , eyes_frames
                ), data