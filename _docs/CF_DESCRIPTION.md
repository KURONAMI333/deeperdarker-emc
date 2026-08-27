# EMC for Deeper and Darker

With this add-on, Deeper and Darker's materials gain EMC and can be used in ProjectE's transmutation system; without it, ProjectE cannot price them. The values are set so that the mod's deep-dark rewards keep their place in progression instead of becoming cheap alternate sources.

## What is valued

Hand-set EMC is placed on the host's core materials, and ProjectE derives the rest from the mod's own vanilla-type recipes.

The backbone follows the order in which the host actually gates its materials: resonarium at 768, warden carapace at 1,024, reinforced echo shard deriving to 5,056, and the sculk catalyst at 8,040. Nothing later in the progression prices below something earlier, so transmutation cannot be used to skip a step.

Gloomsherds sit at 216 so that nine of them line up with the band ProjectE already uses for pottery sherds. Heart of the deep is 4,096, set from the fact that it is a guaranteed warden drop rather than a random one.

## The ancient vase cannot be farmed for profit

Ancient vases are loot containers, which is exactly the shape that breaks EMC economies: if the container is worth less than what falls out of it, opening vases becomes a repeatable gain.

The expected value of a vase's contents was calculated across its loot table and lands between roughly 7,195 and 7,443. The vase is priced at 7,497, above the top of that range, so opening one is never an EMC gain no matter how the roll goes.

## Smithing templates

Both of the host's smithing templates are set to 7,497, the same band vanilla netherite templates occupy. The host lets a template duplicate itself, and that recipe consumes diamonds, which ProjectE prices above 7,497. Duplicating a template therefore costs more than the template is worth, so the self-duplication recipe cannot undercut the value it starts from.

## Dyeing the sculk transmitter

On 1.21.1 the sculk transmitter can be dyed in all sixteen colours. ProjectE learns values by reading vanilla-style recipes, and it does not see these, so this add-on declares all sixteen conversions explicitly, each one counting the transmitter plus the dye that goes into it.

## Differences between the two versions

The 1.21.1 build covers 46 items and the 1.20.1 build covers 33, because several blocks the newer host adds do not exist in the older one.

Echo logs are handled differently for the same reason. On 1.21.1 they are already inside Minecraft's own log tag, so ProjectE prices them at 32 without help; on 1.20.1 that path is missing, so the value is set by hand to the same 32.

The resonarium plate ends up at 3,264 on one version and 3,456 on the other. That gap comes from the host's own recipe differing between the two, and it is left alone rather than forced to match.

## Items intentionally left without EMC

Soul elytra, and the host's tools, weapons, and armour, have no EMC. Durability and enchantments are item state, and transmutation should not erase or recreate it.

Every item the host allows in a composter was checked against vanilla ferns, and all of them price at or below that level, so no composting loop produces free EMC.

## Requirements

- [ProjectE](https://www.curseforge.com/minecraft/mc-mods/projecte) is required.
- [Deeper and Darker](https://www.curseforge.com/minecraft/mc-mods/deeperdarker) is required.
- Minecraft 1.21.1 on NeoForge, and Minecraft 1.20.1 on Forge, are supported.
- This is server-side data; clients do not need to install it.

## License & credits

All Rights Reserved. Free to put in any modpack, on any platform, monetised or not - no permission needed, no credit required. Source is published so you can read exactly what it does.

Author: KURONAMI
