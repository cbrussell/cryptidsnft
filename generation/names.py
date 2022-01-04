import json

f = json.load(open("trait_manifest.json"))

print(f)
data = {}

for a in f:
    # print(a)
    for c in a["categories"]:
        # print(c)
        for fi in c["traits"]:
            # print(fi)

            data[fi["trait"]] = ""


with open(f"names33.json", "w") as w:
    json.dump(data, w, indent=4)
