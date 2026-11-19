import json
from pathlib import Path


ALLOWED_GROUP_TYPES = ("wall", "slab", "trapdoor", "bark", "stairs")
ALLOWED_FILENAME_TYPES = ("slab", "stairs", "trapdoors", "wall")


def filter_recipes():
    filter_version = input("Enter the version to filter recipes by: ").strip()
    recipe_directory = Path(__file__).parent.parent / "versions" / filter_version / "recipe"

    if not recipe_directory.is_dir():
        raise SystemExit(f"Recipe directory not found: {recipe_directory}")

    removed_count = 0
    for recipe_path in recipe_directory.glob("*.json"):
        try:
            recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise SystemExit(f"Could not read {recipe_path}: {error}") from error

        group = recipe.get("group", "")
        has_allowed_group = isinstance(group, str) and any(
            group_type in group for group_type in ALLOWED_GROUP_TYPES
        )
        has_allowed_filename = any(
            filename_type in recipe_path.stem for filename_type in ALLOWED_FILENAME_TYPES
        )
        if not has_allowed_group and not has_allowed_filename:
            recipe_path.unlink()
            removed_count += 1

    print(f"Removed {removed_count} recipe file(s) from {recipe_directory}")


if __name__ == "__main__":
    filter_recipes()