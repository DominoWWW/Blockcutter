import json
from pathlib import Path

import yaml
from beet import Advancement, Context, Recipe


RELEASE_FILE = Path("release.yml")
RECIPE_SUFFIXES = {
	"_slab": 2,
	"_stairs": 1,
	"_wall": 1,
	"_trapdoor": 2,
}
IGNORED_GROUPS = {"wool_slabs", "wool_stairs"}


def _recipe_directory() -> Path:
	with RELEASE_FILE.open(encoding="utf-8") as file:
		release = yaml.safe_load(file)

	return Path("versions") / str(release["minecraft_version"]) / "recipe"


def _item_ids(value: object) -> list[str]:
	if isinstance(value, str):
		return [] if value.startswith("#") else [value.removeprefix("minecraft:")]
	if isinstance(value, dict):
		return _item_ids(value.get("item", value.get("tag", "")))
	if isinstance(value, list):
		item_ids = []
		for item in value:
			item_ids.extend(_item_ids(item))
		return item_ids
	return []


def _ingredients(recipe: dict) -> list[str]:
	key = recipe.get("key", {})
	if key:
		values = key.values()
	else:
		values = recipe.get("ingredients", [])

	return list(dict.fromkeys(
		item_id
		for value in values
		for item_id in _item_ids(value)
	))


def _add_stonecutting_recipe(
	ctx: Context,
	ingredient: str,
	result: str,
	count: int,
) -> None:
	recipe_id = f"minecraft:{result}_from_{ingredient}_stonecutting"
	if recipe_id in ctx.data.recipes:
		return

	ctx.data[recipe_id] = Recipe({
		"type": "minecraft:stonecutting",
		"ingredient": f"minecraft:{ingredient}",
		"result": {
			"id": f"minecraft:{result}",
			"count": count,
		},
	})


def _add_recipe_unlock_advancement(
	ctx: Context,
	output: str,
	ingredient: str,
	recipe_id: str,
) -> None:
	advancement_id = f"blockcutter:recipes/{output}_to_{ingredient}"
	if advancement_id in ctx.data.advancements:
		return

	ctx.data.advancements[advancement_id] = Advancement({
		"criteria": {
			"has_item": {
				"trigger": "minecraft:inventory_changed",
				"conditions": {
					"items": [{"items": [f"minecraft:{output}"]}],
				},
			},
		},
		"rewards": {"recipes": [recipe_id]},
	})


def _add_recipe_back_to_block(
	ctx: Context,
	output: str,
	ingredient: str,
	group: str,
	count: int,
) -> None:
	recipe_id = f"minecraft:{output}_to_{ingredient}"
	if recipe_id in ctx.data.recipes:
		return

	ctx.data[recipe_id] = Recipe({
		"type": "minecraft:crafting_shaped",
		"group": group,
		"category": "building",
		"pattern": ["##"],
		"key": {"#": f"minecraft:{output}"},
		"result": {
			"id": f"minecraft:{ingredient}",
			"count": count,
		},
	})
	_add_recipe_unlock_advancement(ctx, output, ingredient, recipe_id)


def _add_recipes_back_to_block(ctx: Context, recipe: dict, output: str) -> None:
	if recipe.get("type") != "minecraft:crafting_shaped":
		return

	if output.endswith("_slab"):
		group = "slabs_to_block"
		count = 1
	elif output.endswith(("_stairs", "_wall")):
		group = "stairs_to_block" if output.endswith("_stairs") else "walls_to_block"
		count = 2
	else:
		return

	for ingredient in _ingredients(recipe):
		_add_recipe_back_to_block(ctx, output, ingredient, group, count)


def _add_recipes_for_output(ctx: Context, recipe: dict, output: str) -> None:
	if recipe.get("group") in IGNORED_GROUPS:
		return

	_add_recipes_back_to_block(ctx, recipe, output)

	for suffix, count in RECIPE_SUFFIXES.items():
		if output.endswith(suffix):
			for ingredient in _ingredients(recipe):
				_add_stonecutting_recipe(ctx, ingredient, output, count)
			return

	if recipe.get("group") == "bark" and output.endswith(("_wood", "_hyphae")):
		for ingredient in _ingredients(recipe):
			_add_stonecutting_recipe(ctx, ingredient, output, 1)


def create_recipes(ctx: Context):
	for recipe_path in _recipe_directory().glob("*.json"):
		with recipe_path.open(encoding="utf-8") as file:
			recipe = json.load(file)

		output = recipe.get("result", {}).get("id", "")
		if output:
			_add_recipes_for_output(ctx, recipe, output.removeprefix("minecraft:"))
