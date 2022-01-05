import json

trait_manifest = json.load(open("/Users/chrisrussell/CryptidToken/generation/trait_manifest.json"))
color_manifest = json.load(open("/Users/chrisrussell/CryptidToken/generation/color_manifest.json"))

data = {}

for attributes in trait_manifest:
    # print(a)
    for categories in attributes["categories"]:
        # print(c)
        for colors in categories["colors"]:
            # print(fi)
            for color in colors["traits"]:

                data[color["trait"]] = color["trait"]

for colors in color_manifest:
    data[colors["color"]] = colors["color"]

for attributes in trait_manifest:
    data[attributes["attribute"]] = attributes["attribute"]

data["base_color"] = "base_color"
with open("names.json", "w") as w:
    json.dump(data, w, indent=4)

print("Success!")