import json

trait_manifest = json.load(open("/Users/chrisrussell/CryptidToken/generation/trait_manifest.json"))
color_manifest = json.load(open("/Users/chrisrussell/CryptidToken/generation/color_manifest.json"))

data = {}

# get trait names
for attributes in trait_manifest:
    for categories in attributes["categories"]:
        for colors in categories["colors"]:
            for color in colors["traits"]:
                data[color["trait"]] = color["trait"]

# get colors
for colors in color_manifest:
    data[colors["color"]] = colors["color"]

# get attribute names
for attributes in trait_manifest:
    data[attributes["attribute"]] = attributes["attribute"]

# add base color
data["base_color"] = "base_color"

# save json file to be modified
with open("names.json", "w") as w:
    json.dump(data, w, indent=4)

print("Success!")