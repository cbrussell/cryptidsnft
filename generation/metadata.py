import json
import random
import os
import numpy as np

import hidden_metadata

mp4_cid = "QmXtbW1G1nhvNDWTRijEzMaN6eFm6PwhXpbckUuuYE8srb"
still_cid = "QmRyamcnES53h1aKoskqQxeUXkGt8MEm3J5sic4c31jCXV"

def main():
    names = json.load(open("/Users/chrisrussell/CryptidToken/generation/names.json"))
    for filename in os.scandir("/Users/chrisrussell/CryptidToken/generation/output/metadata"):
        if len(filename.name.split(".")) != 2:
            continue
        file_name = filename.name.split(".")[0]
        transformed = transform_json(
            json.load(open(filename.path)), names, file_name
        )

        with open(f"/Users/chrisrussell/CryptidToken/generation/output/new_metadata/{file_name}.json", "w") as o:
            json.dump(transformed, o, indent=4)



def transform_json(data, names, file_name):
    print(file_name)
    metadata = {
        "name": f"Cyptid #{file_name}",
        "description": "",
        "image": f"ipfs://{still_cid}/{file_name}.png",
        "animation_url": f"ipfs://{mp4_cid}/{file_name}.mp4",
        "attributes": []

    }
    for x in data.items():
        
        if x[0] in names.keys():
            print(data.items())
            # For each sub-item in attribute
            print(x[0])
            print(x[1])
            metadata["attributes"].append({"trait_type": names[x[0]], "value": names[x[1]]})
   
    # Boost attributes
    magic = random.randint(50,100)
    empathy = random.randint(50,100)
    morality = random.randint(50,100)
    wisdom = random.randint(50,100)
    chaos = random.randint(50,100)

    metadata["attributes"].append(
            {"display_type": "boost_number", "trait_type": "Magic", "value": magic}
        )
    metadata["attributes"].append(
            {"display_type": "boost_number", "trait_type": "Empathy", "value": empathy}
        )
    metadata["attributes"].append(
            {"display_type": "boost_number", "trait_type": "Morality", "value": morality}
        )
    metadata["attributes"].append(
            {"display_type": "boost_number", "trait_type": "Wisdom", "value": wisdom}
        )
    metadata["attributes"].append(
            {"display_type": "boost_number", "trait_type": "Chaos", "value": chaos}
        )

    return metadata


if __name__ == "__main__":
    main()

