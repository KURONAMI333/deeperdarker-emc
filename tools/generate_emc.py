"""Generate data/deeperdarker/pe_custom_conversions/deeperdarker_default.json
(NeoForge 1.21.1).

Values come from `_research/emc_campaign_2026-08-26/DEEPERDARKER_EMC_SPEC.md`
SS3 (values.before, 43 id) plus the SS8 consolidated rulings: heart_of_the_deep
4096 (SS8-1) and both smithing templates seeded at 7497 (SS8-2) -> **46 ids**.
Every number below is copied from that spec -- this script only encodes the
ProjectE 1.21.1 (PE1.1.0) JSON shape and verifies the written file by reading
it back.

Notable spec rulings baked in here:
- The 16 colored sculk transmitters are NOT hand-set. SculkTransmitterColoring
  is a CustomRecipe subclass keyed by DyeColor, invisible to ProjectE's recipe
  mappers, so they are expressed as a `groups` conversion each:
  transmitter(512) + dye -> colored transmitter (SS4).
- Echo logs (echo_log / echo_wood / stripped_echo_log / stripped_echo_wood)
  are NOT hand-set: `logs_that_burn` pulls them into #minecraft:logs (=32,
  ruling SS0-3). Lint/server verification stays in the next stage.
- GEAR (warden/resonarium equipment incl. sonorous_staff inputs), soul_elytra
  (elytra is unvalued -> undervivable) and ancient_compass (AUTO 2112) are
  intentionally absent.

Usage: python tools/generate_emc.py [--verify-only]
"""

import json
import os
import sys

OUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "src",
    "main",
    "resources",
    "data",
    "deeperdarker",
    "pe_custom_conversions",
    "deeperdarker_default.json",
)

# Hand-set EMC values, SPEC SS3 (+ SS8 rulings). Comment on each id = spec's
# "根拠" column, condensed. (suffix, emc, comment); full id = f"deeperdarker:{suffix}".
BEFORE = [
    # SS3.1 S terrain / P plants & decor (18)
    ("echo_soil", 1, "Otherside surface soil; vanilla dirt(1); self-drops without silk"),
    ("cobbled_gloomslate", 2, "cobble stage of the parent stone; cobbled_deepslate(2)"),
    ("cobbled_sculk_stone", 2, "same as above"),
    ("blooming_sculk_stone", 4, "non-silk break drops cobbled(2) so >=2 required; mossy premium at blackstone/tuff band"),
    ("gloomy_grass", 1, "short_grass(1)"),
    ("glowing_grass", 1, "short_grass(1)"),
    ("glowing_roots", 1, "crimson/warped_roots(1)"),
    ("sculk_tendrils", 4, "sculk_vein(4) anchor"),
    ("sculk_vines", 4, "sculk_vein(4) anchor"),
    ("gloomy_sculk", 16, "ties vanilla sculk's derived 16 (vein x4); silk-only self-drop, place/break neutral"),
    ("gloomy_geyser", 16, "silk-only self-drop decor rock; stepOn only bounces XP orbs, produces no items (javap)"),
    ("bloom_berries", 16, "sweet/glow_berries(16)"),
    ("glowing_flowers", 16, "in minecraft:flowers but PE has no plain-flowers value; small_flowers band by hand"),
    ("ice_lily", 16, "flower band; compost 0.65 merely ties dandelion(16@0.65), not stronger"),
    ("gloomy_cactus", 16, "ruling 7: orange_dye smelting floor of 16, NOT vanilla cactus(8)"),
    ("blooming_moss_block", 12, "moss_block(12); dirt-tag member but PE has no value there, so no double definition"),
    ("porous_sculk_gleam", 12, "moss band; must exceed 2 harvested gleam_gel (8): shearing yields 2x4=8 < 12"),
    ("sculk_gleam", 8, "glow_lichen(8)"),
    # SS3.2 P/D gathers & mob drops (5)
    ("gleam_gel", 4, "ledger '?' resolved: PorousSculkGleamBlock#useItemOn SHEARS_HARVEST yields 2 (javap); 2x4=8 < 12 loss side"),
    ("grime_ball", 16, "clay_ball(16); smelting to grime_brick mirrors clay->brick exactly"),
    ("angler_fish", 64, "minecraft:fishes / c:foods/raw_fish like cod/salmon(64); cooked derives at 64"),
    ("sculk_bone", 144, "bone(144) band; host has ZERO bonemeal recipes from it, so nothing spills into bone_meal"),
    ("soul_dust", 192, "echo_shard(192) band; soundproof_glass = glass(1)+this = 193"),
    # SS3.3 E/M progression materials (8)
    ("crystallized_amber", 32, "amethyst_shard(32) band; worldgen-minable (gloomslate_column) so cheaper than chest/mob-locked carapace (SS7-4); compost 0.65*48=31.2 <= 32"),
    ("sculk_jaw", 64, "secret-chamber trap block; silk-only self-drop; stepOn deals damage only, itemizes nothing (javap)"),
    ("gloomslate_pot", 64, "plain pot breaks back to itself (sherds inserted are the only refund) = neutral; decorated_pot band"),
    ("lite", 64, "loot of enriched_gloomslate_bricks at 1/5; lite_block = 4*lite = 256 derives"),
    ("sculk_transmitter", 512, "ancient_temple_secret exclusive loot; prismarine_crystals band; 16 colors derive via groups (SS4)"),
    ("soul_crystal", 512, "fountain chest + stalker drop; prismarine_crystals band"),
    ("resonarium", 768, "sludge drop (farmable) but the common mid-material of plate/equipment/template; blaze_powder band; above soul_crystal per advancement order"),
    ("warden_carapace", 1024, "warden guaranteed 1-3 + temple/apex + ancient_city 20%; ender_pearl band; main RES ingredient"),
    # SS3.4 T treasure (1)
    ("ancient_vase", 7497, "loot-box EV cap: expected contents ~7195 (1211) < 7497, so buy->smash is EV-negative; netherite-template parity value"),
    # SS3.5 W wood / H sherds (11)
    ("blooming_stem", 32, "#minecraft:logs(32) band; stem->planks is 1->4 so anything below 32 would drag PE's fixed planks(8) down"),
    ("stripped_blooming_stem", 32, "same as above"),
    ("gloomsherd", 216, "pot-mob drop; host tag dd:gloomslate_sherds only -- NOT in vanilla decorated_pot_sherds, so no auto value; hand-set all 9 (ruling 5)"),
    ("brittle_gloomsherd", 216, "see gloomsherd"),
    ("dark_heart_gloomsherd", 216, "see gloomsherd"),
    ("listener_gloomsherd", 216, "see gloomsherd"),
    ("snapper_gloomsherd", 216, "see gloomsherd"),
    ("temple_gloomsherd", 216, "see gloomsherd"),
    ("transmission_gloomsherd", 216, "see gloomsherd"),
    ("ward_gloomsherd", 216, "see gloomsherd"),
    ("wayfinder_gloomsherd", 216, "see gloomsherd"),
    # SS8-1: heart_of_the_deep re-priced (was SKIP before the warden-drop discovery)
    ("heart_of_the_deep", 4096, "ghast_tear band; warden GUARANTEED drop (loot modifier warden_heart_from_warden.json); high-effort kill so no printing; makes craftable sonorous_staff derivable"),
    # SS8-2: smithing templates seeded (self-replication cycles are null-input-ZERO for PE)
    ("warden_upgrade_smithing_template", 7497, "seed for a self-replicating recipe PE cannot resolve (own input in cycle); diamond(8192) > 7497 keeps every derived copy above the seed; vanilla netherite template precedent"),
    ("resonarium_upgrade_smithing_template", 7497, "same as above"),
]

EXPECTED_SHERDS = [
    "gloomsherd", "brittle_gloomsherd", "dark_heart_gloomsherd",
    "listener_gloomsherd", "snapper_gloomsherd", "temple_gloomsherd",
    "transmission_gloomsherd", "ward_gloomsherd", "wayfinder_gloomsherd",
]

DYE_COLORS = [
    "white", "light_gray", "gray", "black", "brown", "red", "orange",
    "yellow", "lime", "green", "cyan", "light_blue", "blue", "purple",
    "magenta", "pink",
]

# SS4.2 verbatim structure: one CustomRecipe keyed by DyeColor, 1 transmitter
# + 1 dye -> 1 colored transmitter. Tag inputs unused.
GROUPS = {
    "sculk_transmitter_coloring": {
        "comment": (
            "deeperdarker:sculk_transmitter_coloring is a custom CraftingRecipe "
            "subclass keyed by DyeColor (SculkTransmitterColoring#assemble uses "
            "DyeColor#getColor and SculkTransmitterItem#getItemByColor), so "
            "ProjectE cannot derive colored variants. One transmitter + one dye "
            "-> one colored transmitter."
        ),
        "conversions": [
            {
                "output": {
                    "type": "projecte:item",
                    "id": f"deeperdarker:{c}_sculk_transmitter",
                },
                "count": 1,
                "ingredients": [
                    {"type": "projecte:item", "id": "deeperdarker:sculk_transmitter"},
                    {"type": "projecte:item", "id": f"minecraft:{c}_dye"},
                ],
            }
            for c in DYE_COLORS
        ],
    }
}

COMMENT = (
    "Deeper and Darker EMC integration for ProjectE (KURONAMI). Values per "
    "_research/emc_campaign_2026-08-26/DEEPERDARKER_EMC_SPEC.md (SS3 + SS8 "
    "rulings). Gear (warden/resonarium armour and the sonorous_staff chain), "
    "stateful curios, soul_elytra (elytra is unvalued) and ancient_compass "
    "(AUTO) intentionally have no EMC. Echo logs ride #minecraft:logs(32). "
    "The 16 colored sculk transmitters derive through the "
    "sculk_transmitter_coloring group."
)


def build_doc() -> dict:
    return {
        "replace": False,
        "comment": COMMENT,
        "values": {
            "before": [
                {"type": "projecte:item", "emc_value": v, "id": f"deeperdarker:{k}"}
                for k, v, _ in BEFORE
            ]
        },
        "groups": GROUPS,
    }


def verify(path: str) -> None:
    """Read back the written JSON and diff it against the in-script SPEC tables."""
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)

    errors: list[str] = []

    got = {
        e["id"]: e["emc_value"]
        for e in doc["values"]["before"]
        if isinstance(e, dict)
        and set(e) == {"type", "emc_value", "id"}
        and e["type"] == "projecte:item"
    }
    if len(got) != len(doc["values"]["before"]):
        errors.append("values.before entries deviate from {type,emc_value,id} shape")

    expected = {f"deeperdarker:{k}": v for k, v, _ in BEFORE}
    for rid in sorted(set(expected) | set(got)):
        if expected.get(rid) != got.get(rid):
            errors.append(f"value mismatch {rid}: expected {expected.get(rid)}, got {got.get(rid)}")

    if len(expected) != 46:
        errors.append(f"SPEC table size is {len(expected)}, expected 46 (43 + heart 1 + templates 2)")

    # positive structure checks
    sherds = [k for k, _, _ in BEFORE if k.endswith("gloomsherd")]
    if sorted(sherds) != sorted(EXPECTED_SHERDS):
        errors.append("gloomsherd enumeration does not match the 9 SPEC SS3.5 ids")
    templates = [k for k, _, _ in BEFORE if k.endswith("_smithing_template")]
    if sorted(templates) != ["resonarium_upgrade_smithing_template", "warden_upgrade_smithing_template"]:
        errors.append("both smithing templates (SS8-2) must be present")
    if expected.get("deeperdarker:heart_of_the_deep") != 4096:
        errors.append("heart_of_the_deep must be hand-set at 4096 (SS8-1)")
    if expected.get("deeperdarker:ancient_vase") != 7497:
        errors.append("ancient_vase must stay at the loot-box EV cap 7497")

    # negative checks: things that must NOT appear in values.before
    forbidden = [
        "echo_log", "echo_wood", "stripped_echo_log", "stripped_echo_wood",
        "sonorous_staff", "soul_elytra", "ancient_compass", "gleam_gel_block",
        "resonarium_plate", "reinforced_echo_shard", "soundproof_glass",
        "lite_block", "bordered_lite_block",
    ]
    leaked = [f"deeperdarker:{n}" for n in forbidden if f"deeperdarker:{n}" in got]
    if leaked:
        errors.append(f"derived/AUTO/GEAR ids leaked into values.before: {leaked}")
    colored_leak = [k for k in got if k.endswith("_sculk_transmitter") and k != "deeperdarker:sculk_transmitter"]
    if colored_leak:
        errors.append(f"colored transmitters must go through groups, not values.before: {colored_leak}")

    # groups checks
    convs = doc["groups"]["sculk_transmitter_coloring"]["conversions"]
    if len(convs) != 16:
        errors.append(f"sculk_transmitter_coloring must hold exactly 16 conversions, got {len(convs)}")
    else:
        for c in convs:
            out_id = c["output"]["id"]
            color = out_id[len("deeperdarker:") : -len("_sculk_transmitter")]
            want_out = {"type": "projecte:item", "id": out_id}
            want_in = [
                {"type": "projecte:item", "id": "deeperdarker:sculk_transmitter"},
                {"type": "projecte:item", "id": f"minecraft:{color}_dye"},
            ]
            if color not in DYE_COLORS:
                errors.append(f"unexpected color in group: {color}")
            elif c["output"] != want_out or c["ingredients"] != want_in or c.get("count") != 1:
                errors.append(f"group conversion mismatch for {color}")
        covered = {c["output"]["id"][len("deeperdarker:") : -len("_sculk_transmitter")] for c in convs}
        if covered != set(DYE_COLORS):
            errors.append("group colors do not cover exactly the 16 DyeColor variants")

    print(f"verify: values.before={len(got)} (expect 46), groups conversions={len(convs)}")
    for k, v, _ in BEFORE:
        mark = "ok" if got.get(f"deeperdarker:{k}") == v else "MISMATCH"
        print(f"  {mark:8s} deeperdarker:{k} = {v}")
    if errors:
        for e in errors:
            print(f"VERIFY FAILED: {e}", file=sys.stderr)
        sys.exit(1)
    print(
        "verify: all 46 ids match DEEPERDARKER_EMC_SPEC.md SS3+SS8; "
        "groups match SS4.2 (16 DyeColor conversions)"
    )


def main() -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if "--verify-only" not in sys.argv[1:]:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(build_doc(), f, ensure_ascii=False, indent=2)
            f.write("\n")
        n_groups = sum(len(g["conversions"]) for g in GROUPS.values())
        print(
            f"values.before={len(BEFORE)} groups.conversions={n_groups} -> {os.path.normpath(OUT)}"
        )
    verify(os.path.normpath(OUT))


if __name__ == "__main__":
    main()
