import json

f = json.load(open("trait_manifest.json"))


data = {}

for a in f:
    # print(a)
    for c in a["categories"]:
        # print(c)
        for fi in c["colors"]:
            # print(fi)
            for color in fi["traits"]:

                data[color["trait"]] = color["trait"]


with open(f"names33.json", "w") as w:
    json.dump(data, w, indent=4)
