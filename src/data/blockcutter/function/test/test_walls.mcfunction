import json
from pathlib import Path

import yaml

with open("release.yml", encoding="utf-8") as file:
    version = yaml.safe_load(file)["minecraft_version"]

recipe_directory = Path("versions") / str(version) / "recipe"
walls = set()
for recipe_path in recipe_directory.glob("*.json"):
    with recipe_path.open(encoding="utf-8") as file:
        output = json.load(file).get("result", {}).get("id", "")
    if output.endswith("_wall"):
        walls.add(output)

for wall in sorted(walls):
    summon minecraft:item ~ ~2 ~ {Item:{id:wall,count:2}}