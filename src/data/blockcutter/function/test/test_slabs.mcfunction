import json
from pathlib import Path

import yaml

with open("release.yml", encoding="utf-8") as file:
    version = yaml.safe_load(file)["minecraft_version"]

recipe_directory = Path("versions") / str(version) / "recipe"
slabs = set()
for recipe_path in recipe_directory.glob("*.json"):
    with recipe_path.open(encoding="utf-8") as file:
        output = json.load(file).get("result", {}).get("id", "")
    if output.endswith("_slab"):
        slabs.add(output)

for slab in sorted(slabs):
    summon minecraft:item ~ ~2 ~ {Item:{id:slab,count:2}}