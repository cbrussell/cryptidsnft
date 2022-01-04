import json

trait_manifest = json.load(open("trait_manifest.json"))

data = {}

for attributes in trait_manifest:
    # print(a)
    for categories in attributes["categories"]:
        # print(c)
        for colors in categories["colors"]:
            # print(fi)
            for color in colors["traits"]:

                data[color["trait"]] = color["trait"]


with open(f"names.json", "w") as w:
    json.dump(data, w, indent=4)
