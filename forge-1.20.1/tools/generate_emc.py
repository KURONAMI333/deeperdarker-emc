"""Generate data/deeperdarker/pe_custom_conversions/deeperdarker_default.json
for ProjectE on Minecraft 1.20.1 (PE1.0.1, Forge).

Values come from `_research/emc_campaign_2026-08-26/DEEPERDARKER_EMC_SPEC.md`
SS5 + the SS8 consolidated rulings.

Cell deltas vs 1.21.1 (all verified against the host jar
deeperdarker-forge-1.20.1-1.3.3 and its survey):
- DROPPED vs SS3: angler_fish (spawn egg only), gleam_gel, gloomsherd x9,
  gloomslate_pot, lite -- none of these items exist on 1.20.1.
- **porous_sculk_gleam does NOT exist on 1.20.1 either** (lang/jar check:
  only `sculk_gleam`). SPEC SS5.1's arithmetic "43 - 13 + 2 = 32" assumed it
  present; with it removed the shared table is 31 ids -> +2 echo logs +2 SS8
  = **33 ids**, not the prose "34". The enumeration (jar reality) is
  authoritative; flagged to the orchestrator, no values changed.
- ADDED by hand: echo_log / stripped_echo_log @ 32 -- item-side
  `logs_that_burn` does not exist on this cell, so PE1.0.1's #minecraft:logs
  (=32) never reaches them (echo_wood / stripped_echo_wood craft from logs).
- ADDED per SS8: heart_of_the_deep @ 4096 and
  warden_upgrade_smithing_template @ 7497 (the ONLY template on this cell;
  there is no resonarium_upgrade_smithing_template here).
- groups: NONE. The transmitter coloring recipe and colored items do not
  exist on 1.20.1 (lang lists the plain transmitter only).

ProjectE 1.20.1's CustomConversionFile reads `values.before` as a MAP
({id: emc}) (PROJECTE_EMC_NOTES.md 1.20.1 table; PE1.0.1 jar's own
defaults/metals JSON). No `output`/`ingredients` fields are emitted since
there are no groups.

Usage: python tools/generate_emc.py [--verify-only]
"""

import json
import os
import sys

OUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "src",
    "data",
    "deeperdarker",
    "pe_custom_conversions",
    "deeperdarker_default.json",
)

# Hand-set EMC values, SPEC SS3 values kept verbatim minus the 1.20.1-only
# drops above. (suffix, emc, comment); full id is f"deeperdarker:{suffix}".
BEFORE = [
    # SS3.1 S terrain / P plants & decor (17 of 18; porous_sculk_gleam absent on 1.20.1)
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
    ("gloomy_geyser", 16, "silk-only self-drop decor rock"),
    ("bloom_berries", 16, "sweet/glow_berries(16)"),
    ("glowing_flowers", 16, "flower band, hand-set"),
    ("ice_lily", 16, "flower band"),
    ("gloomy_cactus", 16, "ruling 7: orange_dye smelting floor of 16, NOT vanilla cactus(8)"),
    ("blooming_moss_block", 12, "moss_block(12)"),
    ("sculk_gleam", 8, "glow_lichen(8)"),
    # SS3.2 P/D gathers & mob drops (3 of 5)
    ("grime_ball", 16, "clay_ball(16); smelting to grime_brick mirrors clay->brick exactly"),
    ("sculk_bone", 144, "bone(144) band"),
    ("soul_dust", 192, "echo_shard(192) band; soundproof_glass = glass(1)+this = 193"),
    # SS3.3 E/M progression materials (6 of 8)
    ("crystallized_amber", 32, "amethyst_shard(32) band; worldgen-minable so cheaper than chest/mob-locked carapace (SS7-4)"),
    ("sculk_jaw", 64, "secret-chamber trap block; silk-only self-drop"),
    ("sculk_transmitter", 512, "ancient_temple_secret exclusive loot; prismarine_crystals band (no colored variants on 1.20.1)"),
    ("soul_crystal", 512, "fountain chest + stalker drop; prismarine_crystals band"),
    ("resonarium", 768, "sludge drop (farmable) mid-material; blaze_powder band; above soul_crystal per advancement order"),
    ("warden_carapace", 1024, "warden guaranteed 1-3 + temple/apex + ancient_city 20%; ender_pearl band"),
    # SS3.4 T treasure (1)
    ("ancient_vase", 7497, "loot-box EV cap: expected contents ~7443 (1201) < 7497, buy->smash is EV-negative"),
    # SS3.5 W wood (4: stems shared + echo logs hand-set on this cell only)
    ("blooming_stem", 32, "#minecraft:logs(32) band; stem->planks is 1->4 so anything below 32 would drag PE's fixed planks(8) down"),
    ("stripped_blooming_stem", 32, "same as above"),
    ("echo_log", 32, "hand-set on 1.20.1: no item-side logs_that_burn tag exists, PE1.0.1 #minecraft:logs never reaches it (SS5.1)"),
    ("stripped_echo_log", 32, "same as above"),
    # SS8-1: heart_of_the_deep re-priced (was SKIP before the warden-drop discovery)
    ("heart_of_the_deep", 4096, "ghast_tear band; warden GUARANTEED drop (warden_heart_from_warden.json); makes craftable sonorous_staff derivable"),
    # SS8-2: the only smithing template that exists on 1.20.1
    ("warden_upgrade_smithing_template", 7497, "seed for a self-replicating recipe PE cannot resolve (own input in cycle); diamond(8192) > 7497 keeps every derived copy above the seed"),
]

EXPECTED_SHERDS_ABSENT = True

COMMENT = (
    "Deeper and Darker EMC integration for ProjectE (KURONAMI). Values per "
    "_research/emc_campaign_2026-08-26/DEEPERDARKER_EMC_SPEC.md (SS5 + SS8 "
    "rulings). Gear (warden armour and the sonorous_staff chain), soul_elytra "
    "(elytra is unvalued) and ancient_compass (AUTO) intentionally have no "
    "EMC. Echo logs are hand-set because 1.20.1 lacks the item-side "
    "logs_that_burn tag. 33 ids total: porous_sculk_gleam/gleam_gel/angler_fish"
    "/gloomsherd x9/gloomslate_pot/lite do not exist on this cell."
)


def build_doc() -> dict:
    return {
        "comment": COMMENT,
        "values": {
            "before": {f"deeperdarker:{k}": v for k, v, _ in BEFORE}
        },
    }


def verify(path: str) -> None:
    """Read back the written JSON and diff it against the in-script SPEC tables."""
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)

    errors: list[str] = []

    before = doc["values"]["before"]
    if not isinstance(before, dict):
        errors.append("values.before must be a MAP {id: emc} on PE1.0.1")
        print(f"VERIFY FAILED: {errors[-1]}", file=sys.stderr)
        sys.exit(1)

    expected = {f"deeperdarker:{k}": v for k, v, _ in BEFORE}
    for rid in sorted(set(expected) | set(before)):
        if expected.get(rid) != before.get(rid):
            errors.append(f"value mismatch {rid}: expected {expected.get(rid)}, got {before.get(rid)}")

    if len(expected) != 33:
        errors.append(
            f"SPEC table size is {len(expected)}, expected 33 "
            "(SS3 43 - porous_sculk_gleam - gleam_gel - angler_fish - 9 sherds "
            "- gloomslate_pot - lite = 31, + 2 echo logs, + heart + warden template)"
        )

    # positive structure checks
    if before.get("deeperdarker:heart_of_the_deep") != 4096:
        errors.append("heart_of_the_deep must be hand-set at 4096 (SS8-1)")
    templates = sorted(k for k in before if k.endswith("_smithing_template"))
    if templates != ["deeperdarker:warden_upgrade_smithing_template"]:
        errors.append(f"exactly one template (warden_upgrade) expected on 1.20.1, got {templates}")
    if before.get("deeperdarker:ancient_vase") != 7497:
        errors.append("ancient_vase must stay at the loot-box EV cap 7497")
    if before.get("deeperdarker:echo_log") != 32 or before.get("deeperdarker:stripped_echo_log") != 32:
        errors.append("echo_log/stripped_echo_log must be hand-set at 32 on 1.20.1")

    # negative checks: things absent from this cell or derived/AUTO/GEAR
    forbidden_absent_cell = [
        "porous_sculk_gleam", "gleam_gel", "gleam_gel_block", "angler_fish",
        "gloomslate_pot", "lite", "lite_block", "bordered_lite_block",
        "resonarium_upgrade_smithing_template",
    ]
    forbidden_derived = [
        "sonorous_staff", "soul_elytra", "ancient_compass",
        "resonarium_plate", "reinforced_echo_shard", "soundproof_glass",
        "echo_wood", "stripped_echo_wood",
    ]
    leaked = [
        f"deeperdarker:{n}"
        for n in (forbidden_absent_cell + forbidden_derived)
        if f"deeperdarker:{n}" in before
    ]
    if leaked:
        errors.append(f"ids that must NOT appear on 1.20.1 leaked into values.before: {leaked}")
    sherds_leak = [k for k in before if k.endswith("gloomsherd")]
    if sherds_leak:
        errors.append(f"gloomsherds do not exist on 1.20.1: {sherds_leak}")

    # groups must be entirely absent on this cell
    if "groups" in doc:
        errors.append("groups must not be emitted on 1.20.1 (no coloring recipe/items exist)")

    print(f"verify: values.before={len(before)} (expect 33), groups=absent")
    for k, v, _ in BEFORE:
        mark = "ok" if before.get(f"deeperdarker:{k}") == v else "MISMATCH"
        print(f"  {mark:8s} deeperdarker:{k} = {v}")
    if errors:
        for e in errors:
            print(f"VERIFY FAILED: {e}", file=sys.stderr)
        sys.exit(1)
    print("verify: all 33 ids match DEEPERDARKER_EMC_SPEC.md SS5+SS8 (jar-reality enumeration)")


def main() -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if "--verify-only" not in sys.argv[1:]:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(build_doc(), f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"values.before={len(BEFORE)} groups=None -> {os.path.normpath(OUT)}")
    verify(os.path.normpath(OUT))


if __name__ == "__main__":
    main()
