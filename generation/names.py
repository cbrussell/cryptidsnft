import json

f = json.load(open("files_manifest.json"))

data = {}

for a in f:
    # print(a)
    for c in a["categories"]:
        # print(c)
        for fi in c["files"]:
            # print(fi)

            data[fi["file"]] = ""


with open(f"names2.json", "w") as w:
    json.dump(data, w)
