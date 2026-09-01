#!/usr/bin/env python3
"""
Immortalers Delight 1.21.1 tag policy:
  - Recipes prefer c: convention tags
  - c: tags list concrete items first, then OPTIONAL #forge:... fallbacks
    (required:false). A missing #forge: must NEVER fail the whole merged c: tag —
    that empties NeoForge/FD contributions pack-wide (Empty Tag in JEI).
  - Do NOT redefine NeoForge-owned tags we don't extend (e.g. c:stones).
  - forge: tags stay concrete-only (no #c: nesting) to avoid cycles
  - Mod-specific tool tags stay immortalers_delight:
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1] / "src" / "main" / "resources" / "data"
RECIPE_DIR = ROOT / "immortalers_delight" / "recipe"


def opt(item_id: str) -> dict:
    return {"id": item_id, "required": False}


def write_tag(path: pathlib.Path, values: list, replace: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"replace": replace, "values": values}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"tag {path.relative_to(ROOT)}")


# --- concrete sets (1.20 gameplay intent) ---

SALAD = [
    "minecraft:carrot",
    "minecraft:beetroot",
    "minecraft:sweet_berries",
    "minecraft:glow_berries",
    "minecraft:red_mushroom",
    "minecraft:brown_mushroom",
    opt("farmersdelight:cabbage"),
    opt("farmersdelight:cabbage_leaf"),
    opt("farmersdelight:tomato"),
    opt("farmersdelight:onion"),
]

VEGETABLES = [
    "minecraft:carrot",
    "minecraft:potato",
    "minecraft:beetroot",
    "minecraft:sweet_berries",
    opt("farmersdelight:cabbage"),
    opt("farmersdelight:cabbage_leaf"),
    opt("farmersdelight:tomato"),
    opt("farmersdelight:onion"),
]

RAW_BEEF = [
    "minecraft:beef",
    opt("farmersdelight:minced_beef"),
    "immortalers_delight:raw_sniffer_steak",
    "immortalers_delight:raw_sniffer_slice",
]
RAW_CHICKEN = ["minecraft:chicken", opt("farmersdelight:chicken_cuts")]
RAW_PORK = ["minecraft:porkchop", opt("farmersdelight:bacon")]
RAW_MUTTON = ["minecraft:mutton", opt("farmersdelight:mutton_chops")]
RAW_MEAT = [
    "minecraft:beef",
    "minecraft:porkchop",
    "minecraft:chicken",
    "minecraft:mutton",
    "minecraft:rabbit",
    opt("farmersdelight:minced_beef"),
    opt("farmersdelight:chicken_cuts"),
    opt("farmersdelight:bacon"),
    opt("farmersdelight:mutton_chops"),
    "immortalers_delight:raw_sniffer_steak",
    "immortalers_delight:raw_sniffer_slice",
]
COOKED_BEEF = [
    "minecraft:cooked_beef",
    opt("farmersdelight:beef_patty"),
    "immortalers_delight:cooked_sniffer_steak",
    "immortalers_delight:cooked_sniffer_slice",
]
COOKED_CHICKEN = ["minecraft:cooked_chicken", opt("farmersdelight:cooked_chicken_cuts")]
COOKED_MEAT = [
    "minecraft:cooked_beef",
    "minecraft:cooked_porkchop",
    "minecraft:cooked_chicken",
    "minecraft:cooked_mutton",
    "minecraft:cooked_rabbit",
    opt("farmersdelight:beef_patty"),
    opt("farmersdelight:cooked_chicken_cuts"),
    opt("farmersdelight:cooked_bacon"),
    opt("farmersdelight:cooked_mutton_chops"),
    "immortalers_delight:cooked_sniffer_steak",
    "immortalers_delight:cooked_sniffer_slice",
]
TOMATO = [opt("farmersdelight:tomato"), opt("farmersdelight:rotten_tomato")]
ONION = [opt("farmersdelight:onion")]
CABBAGE = [opt("farmersdelight:cabbage"), opt("farmersdelight:cabbage_leaf")]
EGG = ["minecraft:egg"]
COOKED_EGG = [opt("farmersdelight:fried_egg"), "immortalers_delight:fried_sniffer_egg"]
DOUGH = [opt("farmersdelight:wheat_dough"), "immortalers_delight:kwat_wheat_dough"]
GRAIN = [
    "minecraft:wheat",
    opt("farmersdelight:rice"),
    "immortalers_delight:evolutcorn",
    "immortalers_delight:evolutcorn_grains",
    "immortalers_delight:kwat_wheat",
    "immortalers_delight:alfalfa",
]
WHEAT_CROP = ["minecraft:wheat"]
WHEAT_SEED = ["minecraft:wheat_seeds"]
MILK = ["minecraft:milk_bucket", opt("farmersdelight:milk_bottle")]
SUGAR = ["minecraft:sugar"]
BREAD = ["minecraft:bread", opt("farmersdelight:wheat_dough")]  # keep bread-ish
MUSHROOM = ["minecraft:brown_mushroom", "minecraft:red_mushroom"]
KNIFE = [
    opt("farmersdelight:flint_knife"),
    opt("farmersdelight:iron_knife"),
    opt("farmersdelight:diamond_knife"),
    opt("farmersdelight:netherite_knife"),
    opt("farmersdelight:golden_knife"),
    "immortalers_delight:bone_knife",
    "#immortalers_delight:tools/immortal_knives",
]
LEATHER = ["minecraft:leather"]
STRING = ["minecraft:string"]
WOODEN_ROD = ["minecraft:stick", "minecraft:bamboo"]
BLAZE_ROD = ["minecraft:blaze_rod"]
ENCHANT_FUEL = ["minecraft:lapis_lazuli", "minecraft:experience_bottle"]
YOGURT = ["immortalers_delight:yogurt"]
RICE = [opt("farmersdelight:rice"), opt("farmersdelight:rice_panicle")]


def with_forge_fallback(concrete: list, *forge_tags: str) -> list:
    """Append forge tag refs as optional so missing forge: never empties c:."""
    out = list(concrete)
    for tag in forge_tags:
        out.append(opt(f"#{tag}"))
    return out


def write_all_tags() -> None:
    # --- c: primary (concrete first, optional forge fallback) ---
    write_tag(ROOT / "c/tags/item/salad_ingredients.json", with_forge_fallback(SALAD, "forge:salad_ingredients"))
    write_tag(ROOT / "c/tags/item/foods/vegetable.json", with_forge_fallback(VEGETABLES, "forge:vegetables"))
    write_tag(ROOT / "c/tags/item/foods/vegetables.json", with_forge_fallback(VEGETABLES, "forge:vegetables"))
    write_tag(ROOT / "c/tags/item/foods/raw_beef.json", with_forge_fallback(RAW_BEEF, "forge:raw_beef"))
    write_tag(
        ROOT / "c/tags/item/foods/raw_chicken.json",
        with_forge_fallback(RAW_CHICKEN, "forge:raw_chicken", "forge:rawchicken"),
    )
    write_tag(ROOT / "c/tags/item/foods/raw_pork.json", with_forge_fallback(RAW_PORK, "forge:raw_pork"))
    write_tag(ROOT / "c/tags/item/foods/raw_mutton.json", with_forge_fallback(RAW_MUTTON, "forge:raw_mutton"))
    write_tag(
        ROOT / "c/tags/item/foods/raw_meat.json",
        with_forge_fallback(
            RAW_MEAT,
            "forge:raw_meat",
            "forge:raw_meats",
            "forge:rawmeat",
            "forge:rawmeats",
            "forge:common_raw_meats",
        ),
    )
    # Legacy flat name some packs still use (NeoForge/FD use c:foods/raw_meat)
    write_tag(
        ROOT / "c/tags/item/raw_meats.json",
        with_forge_fallback(RAW_MEAT + ["#c:foods/raw_meat"], "forge:raw_meats", "forge:raw_meat"),
    )
    write_tag(ROOT / "c/tags/item/foods/cooked_beef.json", with_forge_fallback(COOKED_BEEF, "forge:cooked_beef"))
    write_tag(
        ROOT / "c/tags/item/foods/cooked_chicken.json",
        with_forge_fallback(COOKED_CHICKEN, "forge:cooked_chicken"),
    )
    write_tag(
        ROOT / "c/tags/item/foods/cooked_meat.json",
        with_forge_fallback(COOKED_MEAT, "forge:cooked_meat", "forge:cooked_meats", "forge:cookedmeat", "forge:cookedmeats"),
    )
    write_tag(
        ROOT / "c/tags/item/foods/tomato.json",
        with_forge_fallback(TOMATO, "forge:vegetables/tomato", "forge:crops/tomato"),
    )
    write_tag(ROOT / "c/tags/item/crops/tomato.json", with_forge_fallback(TOMATO, "forge:crops/tomato", "forge:vegetables/tomato"))
    write_tag(ROOT / "c/tags/item/foods/onion.json", ONION)
    write_tag(ROOT / "c/tags/item/foods/cabbage.json", with_forge_fallback(CABBAGE, "forge:crops/cabbage"))
    write_tag(ROOT / "c/tags/item/foods/egg.json", with_forge_fallback(EGG, "forge:eggs"))
    write_tag(ROOT / "c/tags/item/eggs.json", with_forge_fallback(EGG, "forge:eggs"))
    write_tag(ROOT / "c/tags/item/foods/cooked_egg.json", with_forge_fallback(COOKED_EGG, "forge:cooked_eggs"))
    write_tag(ROOT / "c/tags/item/foods/dough.json", with_forge_fallback(DOUGH, "forge:dough"))
    write_tag(ROOT / "c/tags/item/foods/dough/wheat.json", with_forge_fallback(DOUGH, "forge:dough"))
    write_tag(ROOT / "c/tags/item/foods/mushroom.json", with_forge_fallback(MUSHROOM, "forge:mushrooms"))
    write_tag(ROOT / "c/tags/item/grain.json", with_forge_fallback(GRAIN, "forge:grain"))
    write_tag(ROOT / "c/tags/item/crops/wheat.json", with_forge_fallback(WHEAT_CROP, "forge:crops/wheat"))
    write_tag(ROOT / "c/tags/item/seeds/wheat.json", with_forge_fallback(WHEAT_SEED, "forge:seeds/wheat"))
    write_tag(ROOT / "c/tags/item/crops/rice.json", with_forge_fallback(RICE, "forge:crops/rice", "forge:seeds/rice"))
    write_tag(ROOT / "c/tags/item/drinks/milk.json", with_forge_fallback(MILK, "forge:milk"))
    write_tag(ROOT / "c/tags/item/sugar.json", with_forge_fallback(SUGAR, "forge:sugar"))
    write_tag(ROOT / "c/tags/item/bread.json", with_forge_fallback(["minecraft:bread"], "forge:bread", "forge:bread_slices"))
    # Do NOT write c:stones — NeoForge already owns it; a required missing #forge:stone
    # wiped the merged tag for the whole pack (repeater etc.).
    stones_path = ROOT / "c/tags/item/stones.json"
    if stones_path.exists():
        stones_path.unlink()
        print(f"removed {stones_path.relative_to(ROOT)} (leave to NeoForge)")
    write_tag(
        ROOT / "c/tags/item/tools/knife.json",
        with_forge_fallback(KNIFE, "forge:tools/knives"),
    )
    write_tag(ROOT / "c/tags/item/leathers.json", with_forge_fallback(LEATHER, "forge:leather"))
    write_tag(ROOT / "c/tags/item/strings.json", with_forge_fallback(STRING, "forge:string"))
    write_tag(ROOT / "c/tags/item/rods/wooden.json", with_forge_fallback(WOODEN_ROD, "forge:rods/wooden"))
    write_tag(ROOT / "c/tags/item/rods/blaze.json", with_forge_fallback(BLAZE_ROD, "forge:rods/blaze"))
    write_tag(ROOT / "c/tags/item/enchanting_fuels.json", with_forge_fallback(ENCHANT_FUEL, "forge:enchanting_fuels"))
    write_tag(ROOT / "c/tags/item/foods/yogurt.json", with_forge_fallback(YOGURT, "forge:yogurt"))

    # wheat-or-seeds helper used by large_column (no standard single c: tag)
    write_tag(
        ROOT / "c/tags/item/wheat_ingredients.json",
        with_forge_fallback(
            ["minecraft:wheat", "minecraft:wheat_seeds"],
            "forge:wheat_ingredients",
            "forge:crops/wheat",
            "forge:seeds/wheat",
        ),
    )

    # --- forge: concrete only (fallback leaf for c:) ---
    write_tag(ROOT / "forge/tags/item/salad_ingredients.json", SALAD)
    write_tag(ROOT / "forge/tags/item/vegetables.json", VEGETABLES)
    write_tag(ROOT / "forge/tags/item/vegetables/tomato.json", TOMATO)
    write_tag(ROOT / "forge/tags/item/raw_beef.json", RAW_BEEF)
    write_tag(ROOT / "forge/tags/item/raw_chicken.json", RAW_CHICKEN)
    write_tag(ROOT / "forge/tags/item/rawchicken.json", RAW_CHICKEN)
    write_tag(ROOT / "forge/tags/item/raw_pork.json", RAW_PORK)
    write_tag(ROOT / "forge/tags/item/raw_mutton.json", RAW_MUTTON)
    write_tag(ROOT / "forge/tags/item/raw_meat.json", RAW_MEAT)
    write_tag(ROOT / "forge/tags/item/raw_meats.json", RAW_MEAT)
    write_tag(ROOT / "forge/tags/item/rawmeat.json", RAW_MEAT)
    write_tag(ROOT / "forge/tags/item/rawmeats.json", RAW_MEAT)
    write_tag(ROOT / "forge/tags/item/common_raw_meats.json", RAW_MEAT)
    write_tag(ROOT / "forge/tags/item/cooked_beef.json", COOKED_BEEF)
    write_tag(ROOT / "forge/tags/item/cooked_chicken.json", COOKED_CHICKEN)
    write_tag(ROOT / "forge/tags/item/cooked_meat.json", COOKED_MEAT)
    write_tag(ROOT / "forge/tags/item/cooked_meats.json", COOKED_MEAT)
    write_tag(ROOT / "forge/tags/item/cookedmeat.json", COOKED_MEAT)
    write_tag(ROOT / "forge/tags/item/cookedmeats.json", COOKED_MEAT)
    write_tag(ROOT / "forge/tags/item/eggs.json", EGG)
    write_tag(ROOT / "forge/tags/item/cooked_eggs.json", COOKED_EGG)
    write_tag(ROOT / "forge/tags/item/dough.json", DOUGH)
    write_tag(ROOT / "forge/tags/item/mushrooms.json", MUSHROOM)
    write_tag(ROOT / "forge/tags/item/grain.json", GRAIN)
    write_tag(ROOT / "forge/tags/item/crops/wheat.json", WHEAT_CROP)
    write_tag(ROOT / "forge/tags/item/seeds/wheat.json", WHEAT_SEED)
    write_tag(ROOT / "forge/tags/item/crops/tomato.json", TOMATO)
    write_tag(ROOT / "forge/tags/item/crops/cabbage.json", CABBAGE)
    write_tag(ROOT / "forge/tags/item/crops/rice.json", RICE)
    write_tag(ROOT / "forge/tags/item/milk.json", MILK)
    write_tag(ROOT / "forge/tags/item/sugar.json", SUGAR)
    write_tag(ROOT / "forge/tags/item/bread.json", ["minecraft:bread"])
    write_tag(ROOT / "forge/tags/item/leather.json", LEATHER)
    write_tag(ROOT / "forge/tags/item/string.json", STRING)
    write_tag(ROOT / "forge/tags/item/rods/wooden.json", WOODEN_ROD)
    write_tag(ROOT / "forge/tags/item/rods/blaze.json", BLAZE_ROD)
    write_tag(ROOT / "forge/tags/item/enchanting_fuels.json", ENCHANT_FUEL)
    write_tag(ROOT / "forge/tags/item/yogurt.json", YOGURT)
    write_tag(ROOT / "forge/tags/item/wheat_ingredients.json", ["minecraft:wheat", "minecraft:wheat_seeds"])
    write_tag(ROOT / "forge/tags/item/beef_or_pork.json", ["minecraft:beef", "minecraft:porkchop", opt("farmersdelight:minced_beef"), opt("farmersdelight:bacon")])

    # immortalers aliases → c (thin); forge refs optional
    write_tag(ROOT / "immortalers_delight/tags/item/salad_ingredients.json", ["#c:salad_ingredients"])
    write_tag(ROOT / "immortalers_delight/tags/item/vegetables.json", ["#c:foods/vegetable", "#c:foods/vegetables"])
    write_tag(ROOT / "immortalers_delight/tags/item/common_raw_meats.json", ["#c:foods/raw_meat"])
    write_tag(
        ROOT / "immortalers_delight/tags/item/beef_or_pork.json",
        ["#c:foods/raw_beef", "#c:foods/raw_pork", opt("#forge:raw_beef"), opt("#forge:raw_pork")],
    )
    write_tag(ROOT / "immortalers_delight/tags/item/wheat_ingredients.json", ["#c:wheat_ingredients"])


# Recipe tag remaps: forge / immortalers food → c
TAG_REMAP = {
    "forge:salad_ingredients": "c:salad_ingredients",
    "forge:vegetables": "c:foods/vegetable",
    "forge:vegetables/tomato": "c:foods/tomato",
    "forge:grain": "c:grain",
    "forge:leather": "c:leathers",
    "forge:string": "c:strings",
    "forge:rods/wooden": "c:rods/wooden",
    "forge:rods/blaze": "c:rods/blaze",
    "forge:enchanting_fuels": "c:enchanting_fuels",
    "forge:yogurt": "c:foods/yogurt",
    "forge:raw_beef": "c:foods/raw_beef",
    "forge:raw_chicken": "c:foods/raw_chicken",
    "forge:rawchicken": "c:foods/raw_chicken",
    "forge:raw_pork": "c:foods/raw_pork",
    "forge:raw_meat": "c:foods/raw_meat",
    "forge:raw_meats": "c:foods/raw_meat",
    "forge:common_raw_meats": "c:foods/raw_meat",
    "forge:cooked_beef": "c:foods/cooked_beef",
    "forge:cooked_chicken": "c:foods/cooked_chicken",
    "forge:eggs": "c:eggs",
    "forge:dough": "c:foods/dough",
    "forge:mushrooms": "c:foods/mushroom",
    "forge:milk": "c:drinks/milk",
    "forge:sugar": "c:sugar",
    "forge:crops/rice": "c:crops/rice",
    "forge:crops/tomato": "c:crops/tomato",
    "forge:crops/cabbage": "c:foods/cabbage",
    "forge:wheat_ingredients": "c:wheat_ingredients",
    "forge:beef_or_pork": "immortalers_delight:beef_or_pork",  # resolved via c inside that tag
    "immortalers_delight:salad_ingredients": "c:salad_ingredients",
    "immortalers_delight:vegetables": "c:foods/vegetable",
    "immortalers_delight:common_raw_meats": "c:foods/raw_meat",
    "immortalers_delight:wheat_ingredients": "c:wheat_ingredients",
    # beef_or_pork: keep immortalers tag name but it now points at c:+forge fallbacks
}


def remap_ingredient(obj: object) -> tuple[bool, object]:
    changed = False
    if isinstance(obj, dict):
        if "tag" in obj and isinstance(obj["tag"], str):
            old = obj["tag"]
            new = TAG_REMAP.get(old)
            if new and new != old:
                obj = dict(obj)
                obj["tag"] = new
                changed = True
        # special: beef_or_pork as compound of c beef + c pork (c first)
        if obj.get("tag") == "immortalers_delight:beef_or_pork":
            obj = {
                "type": "neoforge:compound",
                "children": [
                    {"tag": "c:foods/raw_beef"},
                    {"tag": "c:foods/raw_pork"},
                ],
            }
            changed = True
        out = {}
        for k, v in obj.items():
            sub_c, sub_v = remap_ingredient(v)
            changed = changed or sub_c
            out[k] = sub_v
        return changed, out
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            sub_c, sub_v = remap_ingredient(item)
            changed = changed or sub_c
            new_list.append(sub_v)
        return changed, new_list
    return False, obj


def fix_recipes() -> int:
    fixed = 0
    for path in sorted(RECIPE_DIR.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        changed, data = remap_ingredient(data)
        if changed:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            fixed += 1
            print(f"recipe {path.relative_to(ROOT)}")
    return fixed


def audit_remaining() -> None:
    forge_hits = []
    for path in RECIPE_DIR.rglob("*.json"):
        text = path.read_text(encoding="utf-8-sig")
        for m in re.finditer(r'"tag"\s*:\s*"(forge:[^"]+)"', text):
            forge_hits.append(f"{path.name}: {m.group(1)}")
        for m in re.finditer(r'"tag"\s*:\s*"(immortalers_delight:(?!tools/)[^"]+)"', text):
            forge_hits.append(f"{path.name}: {m.group(1)}")
    print("--- remaining forge / non-tool immortalers tags in recipes ---")
    if not forge_hits:
        print("(none)")
    else:
        for h in forge_hits:
            print(h)


def main() -> None:
    write_all_tags()
    n = fix_recipes()
    print(f"updated {n} recipes")
    audit_remaining()


if __name__ == "__main__":
    main()
