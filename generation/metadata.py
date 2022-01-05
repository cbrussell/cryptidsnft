import json
import random
import os
import numpy as np

import hidden_metadata

animation_cid = "QmZZrU4frUkddeZAnYKz4Ti63YHhDZNtqyPWDC6WMhh1dy"


def main():
    names = json.load(open("names.json"))
    for filename in os.scandir("/Users/chrisrussell/CryptidToken/generation/output/metadata"):
        if len(filename.name.split(".")) != 2:
            continue
        transformed = transform_json(
            json.load(open(filename.path)), names, filename.name.split(".")[0]
        )

        with open(filename, "w") as o:
            json.dump(transformed, o, indent=4)


def transform_json(data, names, file_name):
    print(file_name)
    metadata = {
        
        "name": f"Cyptid #{file_name}",
        "description": "",
        "image": f"ipfs://{animation_cid}/{file_name}.mp4",
        "attributes": []

    }
    for x in data.items():
        # For each sub-item in attribute
        print(x)
        for y in x:
            print(y)
            print(x[1])
            metadata["attributes"].append(
                {"trait_type": names[x[0]], "value": names[y]}
            )
   
    # Boost attributes
    magic = random.randint(50,101)
    empathy = random.randint(50,101)
    morality = random.randint(50,101)
    wisdom = random.randint(50,101)
    chaos = random.randint(50,101)

    metadata["attributes"].append(
            {"boost_number": "Magic", "value": magic}
        )
    metadata["attributes"].append(
            {"boost_number": "Empathy", "value": empathy}
        )
    metadata["attributes"].append(
            {"boost_number": "Morality", "value": morality}
        )
    metadata["attributes"].append(
            {"boost_number": "Wisdom", "value": wisdom}
        )
    metadata["attributes"].append(
            {"boost_number": "Chaos", "value": chaos}
        )

    return metadata


if __name__ == "__main__":
    main()

