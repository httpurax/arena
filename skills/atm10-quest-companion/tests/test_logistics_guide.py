#!/usr/bin/env python3
"""Offline tests for references/logistics-guide.md (atm10-quest-companion).

Stdlib-only and network-free: the page is a static Markdown file, so every case reads it
from disk and checks it against constants transcribed from the pack's own config at the
pinned commit (AllTheMods/ATM-10 ``main`` @ e5e3d1d83e, pack 8.2, 2026-09-22), against the
pack's shipped ``config/*.toml`` files, and against the skill's example chapter list.

Covered:

  * existence and grounding: the page is not a stub, states the skill's grounding rules
    (in-game quest book + JEI authoritative, judgement labelled, nothing invented, no
    recipes), names every pack file it was read from, and dates itself to the pinned
    commit, ``CHANGELOG.md``, pack 8.2, and the skill's 8.x stamp;
  * the group's shape: the four Logistics chapters (filename, book title, group, order,
    quest count, chapter id, icon) and the untitled/optional counts the page prints,
    cross-checked against ``examples/progress.example.json``;
  * key content: every cited quest id, title, and subtitle (104 of them, including the
    eight *Mekanism* transport quests the page borrows); the 162 sentences quoted from the
    chapters' own descriptions; the mod names and versions from ``config/crash_assistant/
    modlist.json``; the shipped ``integrateddynamics``/``integratedtunnels``/``pylons``
    config values; and the three lag parentheticals the page leans its ranking on;
  * grounding guards: every ``namespace:name`` id on the page is one the config writes, no
    transport mod the pack does not quest is smuggled in, the untitled quests are marked
    rather than renamed, the judgement labels survive, and every sibling doc the page
    points at exists;
  * the rest of the skill points at the page (SKILL.md routing, grounding note, completion
    checklist, version bump), and this suite imports no network module.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
GUIDE_MD = REFERENCES / "logistics-guide.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"

# Where the page was read from: the pack's quest config, its shipped mod configs, and its
# mod list, all at the same pinned commit as the sibling docs.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters/basic_logistics.snbt",
    "config/ftbquests/quests/chapters/integrated_dynamics.snbt",
    "config/ftbquests/quests/chapters/modular_router.snbt",
    "config/ftbquests/quests/chapters/pylons.snbt",
    "config/ftbquests/quests/chapters/mekanism.snbt",
    "config/ftbquests/quests/chapter_groups.snbt",
    "lang/en_us/chapters",
    "config/ftbquests/quests/lang/en_us/chapter.snbt",
    "config/integrateddynamics-common.toml",
    "config/integratedtunnels-common.toml",
    "config/integratedterminals-common.toml",
    "config/integratedcrafting-common.toml",
    "config/pylons-server.toml",
    "config/crash_assistant/modlist.json",
    "config/bcc-common.toml",
)
PINNED_COMMIT = "e5e3d1d83e"
PINNED_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"

# The quest-book group this page is about: id and title from chapter_groups.snbt +
# lang/en_us/chapter_group.snbt. It holds exactly these four chapters.
GROUP_ID = "3D4E23B1100491AB"
GROUP_TITLE = "Logistics"

# filename -> (book title, group, order_index, quest count, chapter id, icon, quests with no
# title in the lang file, quests flagged optional). Read from the four chapter files and
# lang/en_us/chapter.snbt at the pinned commit; the title/group/stage columns are re-checked
# against examples/progress.example.json below.
CHAPTER_FACTS = {
    "basic_logistics": ("Basic Logistics", "Logistics", 0, 40, "3DEB33F78398EAD6",
                        "pipez:wrench", 21, 6),
    "integrated_dynamics": ("Integrated Dynamics", "Logistics", 1, 28, "69299302373C4CBC",
                            "integrateddynamics:crystalized_menril_chunk", 24, 6),
    "modular_router": ("Modular Routers", "Logistics", 2, 55, "0AB4F9AED808DE48",
                        "modularrouters:modular_router", 48, 1),
    "pylons": ("Pylons", "Logistics", 3, 13, "5712300EF4E5E846",
               "pylons:infusion_pylon", 12, 1),
}
TOTAL_QUESTS = sum(row[3] for row in CHAPTER_FACTS.values())          # 136
TOTAL_UNTITLED = sum(row[6] for row in CHAPTER_FACTS.values())        # 105

# The hidden author-credit quest every chapter of the group carries (optional, two checkmark
# tasks, no rewards).
CREDIT_QUESTS = ("230582AAFC0A1632", "6ABDBE41880CFDA9", "2BB5769119BA2472",
                 "5E02AE661945306C")

# modlist.json at the commit: name -> version, for every mod this page describes.
MOD_VERSIONS = {
    "Pipez": "1.21.1-1.2.31",
    "LaserIO": "1.9.11",
    "IntegratedDynamics": "1.37.1",
    "IntegratedTunnels": "1.12.0",
    "IntegratedTerminals": "1.10.0",
    "IntegratedCrafting": "1.7.2",
    "IntegratedScripting": "1.0.27",
    "Modular Routers": "13.2.7",
    "Mekanistic Routers": "1.2.0",
    "Pylons": "5.4.2",
    "FTB Filter System": "21.1.4",
    "Transfer Labels": "0.1.9",
    "Mekanism": "10.7.19",
}
# Total mods in the same file, which the page quotes as the size of the mod list.
MODLIST_COUNT = "489"

# Mods that ship transport (or a transport-adjacent) content but are never quested in this
# group; the page may only mention them as *installed and unquested*, named by jar.
UNQUESTED_JARS = ("enderio-8.2.12-beta.jar", "logisticsnetworks-1.21.1-1.16.3.jar",
                  "mekanisticrouters-1.2.0.jar", "integratedscripting-1.21.1-neoforge-1.0.27.jar")

# The pack writes no config file for these, so the mods run on defaults (verified by listing
# the commit's config/ directory).
NO_SHIPPED_CONFIG = ("Pipez", "LaserIO", "Modular Routers", "Transfer Labels")
# …while these do get a file from the pack, which the mod table must name.
HAS_SHIPPED_CONFIG_TOML = ("IntegratedDynamics", "IntegratedTunnels", "IntegratedTerminals",
                           "IntegratedCrafting", "Pylons")

# The three parentheticals the page's ranking rests on, verbatim from
# lang/en_us/chapters/basic_logistics.snbt. They are the only ordering the pack states.
LAG_NOTES = (
    "(Can be laggy when used in mass, still not as laggy as Mekanism pipes though).",
    "(These can cause a bit of lag when used in mass so be careful with them).",
    "(Least laggy pipe solution, these are recommended).",
)

# Shipped config values the page quotes: file -> (setting, value). From
# config/integrateddynamics-common.toml, config/integratedtunnels-common.toml, and
# config/pylons-server.toml at the pinned commit.
CONFIG_VALUES = {
    "integrateddynamics-common.toml": (
        ("energyRateLimit", "2147483647"),
        ("ingredientNetworkObserverFrequencyMin", "5"),
        ("ingredientNetworkObserverFrequencyMax", "40"),
        ("defaultPartUpdateFreq", "1"),
        ("maxPartOffset", "32"),
        ("safeMode", "false"),
        ("recreateCorruptedNetworks", "true"),
        ("logChangeEvents", "false"),
        ("analytics", "false"),
        ("filledMenrilLogChance", "10"),
    ),
    "integratedtunnels-common.toml": (
        ("fluidRateLimit", "2147483647"),
        ("inventoryUnchangedTickTimeout", "10"),
        ("ejectItemsOnBlockDropOverflow", "true"),
        ("ejectItemsOnInconsistentSimulationMovement", "true"),
    ),
    "pylons-server.toml": (
        ("harvesterWorkDelay", "20"),
        ("harvesterRequiresTool", "true"),
        ("harvesterCanBeAutomated", "false"),
        ("harvesterRequiresPower", "false"),
        ("infusionChunkloads", "true"),
        ("infusionMinimumDuration", "60"),
        ("infusionRequiredDuration", "3600"),
        ("infusionMaximumPotency", "3"),
        ("expulsionPylonMaxRadius", "2"),
        ("expulsionPylonCanExplode", "false"),
        ("teamSupportEnabled", "true"),
    ),
}
# The one place the pack deviates from a mod default, which the page must present as such.
PACK_CHANGED_DEFAULT = ("harvesterWorkDelay", "20", "60")

# Names a logistics page could plausibly reach for and the pack's four chapters never contain
# (checked against every title, subtitle, and description of basic_logistics,
# integrated_dynamics, modular_router, and pylons at the pinned commit).
UNVERIFIED_NAMES = (
    "Conduit Binder",
    "Thermal Ducts",
    "Refined Pipes",
    "Logistics Pipes",
    "Item Collector",
    "Tier 2 Logistics",
)

# The page's sections, in the order the sibling guides use.
SECTION_ORDER = (
    "## The short answer",
    "## Provenance — everything here was read, not remembered",
    "## Grounding rules (read before repeating any of this)",
    "## The Logistics group at a glance",
    "## What the book says logistics is",
    "## The options, as the chapter is arranged",
    "## 1. Pipez — the five pipes",
    "## 2. Mekanism transport — Advanced tier, handed out",
    "## 3. LaserIO — nodes, cards, filters, overclockers",
    "## 4. Integrated Dynamics — the option the pack calls least laggy",
    "## 5. Modular Routers — transport with no pipes at all",
    "## 6. Pylons — filed under Logistics, moves nothing",
    "## 7. Transfer Labels — a pipe that fits in one block of space",
    "## Which one to build, and when *(judgement)*",
    "## What the pack ships for these mods (and what it does not)",
    "## Related pages",
    "## What this page deliberately does not tell you",
    "## Using this page in a session",
)

# Sibling docs the page must point at, and which must exist.
SIBLING_DOCS = (
    "automation-first-steps.md",
    "storage-ladder.md",
    "power-guide.md",
    "ore-processing-ladder.md",
    "farming-guide.md",
    "chunk-loading-guide.md",
    "lag-fix-guide.md",
    "autocrafting-guide.md",
    "mob-farm-progression.md",
    "key-mods.md",
    "progression.md",
)

QUOTED_SENTENCES = (
    "Pipez is the simplest Logistics Mod.",
    "(Can be laggy when used in mass, still not as laggy as Mekanism pipes though).",
    "(These can cause a bit of lag when used in mass so be careful with them).",
    "(Least laggy pipe solution, these are recommended).",
    "This quest is intentionally hidden, if you're seeing this, you're in editing mode.",
    "Logistics: A system of moving, managing, and storing items or resources. In Modded Minecraft it's quite the same, moving items! With Modded you will need items and by the thousands, heck if you want the Star it gets in the millions! So you'll need to move items from factories, machines, farms, and especially chests. That's what Logistics is for.",
    "LaserIO is DireWolf's continuation of EnderIO's Logistics.",
    "Ever wanted to fit a pipe between blocks?",
    "Attach the specific Pipe to where you want to move items and use the Pipe Wrench to configure what side Pulls, Pushes, or doesn't connect.",
    "Other Wrenches do work with Pipez as well!",
    "It will move Items from one Inventory to another. Could be from one Chest to another, could be a Farm to a System, or even a Quarry to a Smelter.",
    "This can be connected to Sinks to move Infinite Water!",
    "Every Tech Mod needs Energy, whether it's FE, RF or something else!",
    "Some Machines have strict IO ports for Energy so make sure to check for those!",
    "They can move Items, Fluids, or Energy.",
    "Gas can't be moved with any of the other Pipez so if you need to move Hydrogen or Lithium you'll need Gas Pipez.",
    "(I've always had problems telling whether the Mekanism item is Gas, Fluid, or even Infuse Type.",
    "If it doesn't you can check JEI for other recipes that might involve it!)",
    "Pipez do have their own way of Filtering Items, you need atleast an Advanced Upgrade to get it though.",
    "To set it, Shift Right Click an Inventory with it.",
    "All Upgrades increase the amount the Pipez move and also grant more options to use with the Pipe.",
    "Basic Upgrade allows Redstone Activation with Pipez, to change distribution either:Closest First, Farthest First, Round-Robin, or Random, and to add Filters.",
    "Improved, Advanced, and Ultimate upgrades don't grant anything new they just move more!",
    "The different Machines are picky with Configurations and will need to be changed in their GUI to properly move items. Then you can use the Meka Pipes to move whatever you need to move! But wait it's not just Mekanism these work for! They work for plenty of other machines as well! Just need to be Configured with a Wrench to Push and Pull.",
    "Logical Transporters are what Meka uses to move Items and Blocks across distance.",
    "Mechanical Pipes are how Meka lets the Fluids flow.",
    "Mekanism is Tech Mod... why are you surprised it needs Energy for its Machines?",
    "Thermal Evaporation Plants and Fusion Reactors both use Heat to work. And Conductors is how you will be moving Heat!",
    "Gases are the main ones as if you're using Mekanism you will be using Gases like Hydrogen and Oxygen.",
    "Slurries are used with Ore Processing.",
    "Infuse Types are similar like Coal Infuse and Redstone Infuse",
    "Slurries are used with Ore Processing",
    "Dye Pigments are the essence of Color",
    "Basic: will move 2 Blocks/Items across 1 Block each Second.",
    "Ultimate: will move 2 stacks of Items or Blocks across 10 Blocks each Second.",
    "Basic: will hold 2 Buckets of Fluids and move 250mB of Fluid each Tick.",
    "Ultimate: will hold 128 Buckets and will move 32 Buckets each Tick.",
    "Basic: will hold and move 3.2kFE per Tick.",
    "Ultimate: will hold and move 3.27mFE per Tick.",
    "Basic: will hold 4 Buckets of Chemicals and move 750mB of Chemicals each Tick.",
    "I'm not sure what these numbers mean but following the pattern: more expensive, more good!",
    "If you use it on Pipes it will change if they Push, Pull, or Both. You can use it on Ports to set Inputs and Outputs. And even on Bins to set them to Auto-Export below them.",
    "You like Drawers? Mekanism gives us some! Just these are called Bins.",
    "Ultimate: holds 4,096 Stacks.",
    "With 2 Quantum Entangloporters we can Wirelessly move Items, Fluids, Chemicals, Heat, and Energy!",
    "Oh come on this is just Magic!",
    "LaserIO is DireWolf's continuation of EnderIO's Logistics. It's all about moving items via Lasers! Who doesn't love Lasers?! And it all starts with the Logic Chip.",
    "These are just used to Connect Laser Nodes to each other and to Connectors.",
    "Now this is the true Heart of LaserIO! The Laser Nodes are where the actual Cards will go into in order to work.",
    "They will move Items from any adjacent Inventory in the 4 Cardinal Directions and Up and Down.",
    "Set one to Extract and put it on the side of the Laser Node you want to Import from. Then set the other to Insert and put it to the side you want the Items to Export to.",
    "Works exactly like the Item Cards, you need Extract and Insert Cards.",
    "No, it doesn't move Sources of Fluid in or out of the World.",
    "Energy has to get around somehow, preferably where we want it to go.",
    "If we can have Wireless FE why not Wireless Redstone?",
    "Everything Pressurized Tubes can move, these cards can. Gas, Infuse Types, and Pigments.",
    "Simply put Items into it and they are now filtered.",
    "Matching NBT Data would mean having same Enchantments, Durabilitiy, or even Mobs inside of whatever Item.",
    "But instead of only being that Item it will be any Item from that Mod.",
    "(You can also find Tags by doing /kubejs hand to find what's the Tags of the Item in your hand.)",
    "It will then wait until that set Number of Items is there to start taking Items. It will also leave that amount in the first Inventory.",
    "You can store multiple Cards in it and when you open a Laser Node the Card Holder will open up as well like a second Inventory.",
    "Left Click a Card with the Cloner to copy its Data, then Right Click a Card to give it that Data!",
    "If you need to string your Laser Nodes a far distance try using Connectors!",
    "Cards have their limits. Item Extration can only extract 8 items per Operation. Fluid Extract at only 5 Buckets.",
    "These go into the Node itself on bottom right and boost how fast it does Operations.",
    "Integrated Dynamics is all about Logistics! It's practically the definition of Logistic. It's all about moving, managing, and storing items. Heck you might not even need the Wrench for it, it's so well designed! Get one just incase though.",
    "Logic Cables are different from other Pipez or Meka pipes. The other Pipes act as hoppers, the items move from 1 Inventory, into the Pipe, then into the 2nd Inventory. Logic Cables just skip the middle man which also skips a lotta lag.",
    "It can be changed to Import Items at the Integer Limit (Over 2 Billion).",
    "I do have to say I found it having problems with Importing or Exporting to Flux Plugs and Points so be mindful of that.",
    "Does not place or take Fluid Sources from in the world, it only moves Fluids from one Tank to another.",
    "Integrated Dynamics (ID) is a logistics mod that can be used for storage, item/power/fluid transfer and more! Menril trees can be found in Meneglin biomes.",
    "read the guidebook given as a reward for this quest if you want to go further in depth.",
    "Jump on the Squeezer to turn them into Menril Resin.",
    "You can empty the Squeezer by giving it a Redstone signal.",
    "After 7.5 seconds the Menril Resin will turn into a Block of Crystallized Menril.",
    "These chunks are the main crafting ingredient of ID.",
    "They are just for connecting Importers and Interfaces.",
    "You can change how much is Importer, which Item Slot, which Channel, practically everything with just that Card.",
    "Put an Importer onto the inventory you want stuff pulled from.",
    "Works like Importers do, only they export instead.",
    "You can think of this like an AE2 Storage Bus.",
    "The Logic Programmer lets you set the value of variables.",
    "Same thing as Logic Programmer, only this one can be used anywhere.",
    "Place a Crafting Interfaces on a crafting table and right-click on it, this will give you some slots for Variable Cards.",
    "Shows which crafting recipes are happening at any time.",
    "The Energy Battery lets you store FE. To transfer it, you will need Energy Interfaces.",
    "The Generator generates FE using burnable fuels like Coal.",
    "The Wrench is used to rotate or destroy certain blocks, shift right-click in the air to change modes.",
    "It's time to move stuff from one place to another. Here are the steps: 1. Place an interface on an inventory (like a Chest or a Tank) 2. Place an Importer or an Exporter on another inventory, depending on whether you want to pull or send stuff to it. 3. Hook the both up with Cables, place a Variable Card into the Importer or Exporter, and there you go!",
    "Ticks/Operation: If an interface is set to 10 ticks/operation, it will import/export once every 10 ticks (0.5 seconds).",
    "Priority: Sends items to the inventory with the higher priority interface on it.",
    "Item/Energy Channels: This will split your system into multiple channels.",
    "In here you can change transfer rates to be able to send INFINITE items/fluids/energy, as well as being able to do some other stuff.",
    "Menril Seeds can be used to automate Menril Berries, Menril Logs and Menril Saplings.",
    "Menril Bees can be used to automate Crystallized Menril Chunks.",
    "Integer Limit (Over 2 billion)",
    "The fastest possible frequency in ticks at which ingredient network should be observed.",
    "The slowest possible frequency in ticks at which ingredient network should be observed.",
    "How many ticks importers/exporters should sleep until checking targets again when they were previously unchanged.",
    "Will be voided otherwise",
    "If disabled, items can be voided.",
    "When enabled, networks will stop ticking and values will not be shown and evaluated again. This can be used to fix crashing networks by temporarily enabling this option",
    "If corrupted networks should automatically be restored on first tick.",
    "Also the Buffer is the single item slot in the Router where items will come and go through. And it will need Redstone signal for most modules to work.",
    "Modules determine the action the Router preforms.",
    "Filtering and Upgrades go into the Modules themselves.",
    "Upgrades go directly into the Router and the Router can hold 5 of them.",
    "Augments are similar to Upgrades but for the individual Modules!",
    "And it will need Redstone signal for most modules to work",
    "A Router does it's action every time it has one of it's ticks.",
    "Default is 20 Ticks or 1 Second.",
    "1 Stack Upgrade is 2 Items, 2 Stacks 4 Items, and 6 Stacks is 64 Items a second.",
    "This does not stack with Upgrades though... infact it overrides them.",
    "will only move items into Inventories on the same XYZ axis as the Router and with direct line of sight. If there is a block in the way, the MK1 Sender will not send.",
    "MK2 doesn't need direct line of sight or to be on same XYZ axis. Will have to be in the same Dimension though, unless you have...",
    "MK3 doesn't worry about XYZ axis, line of sight, or Dimension. As long as the Inventory is in the same Minecraft World it can move items into it.",
    "The Inventory has to be adjacent to the Router",
    "Just not only from adjacent Inventories, but any Inventory nearby!",
    "Any items that come into the Router, will be deleted forever!",
    "Recommend using Filters with this one...",
    "It's my stuff, no touchy.",
    "Only you can use and mess with the Router after putting in the Upgrade.",
    "TNT won't break it, Wither won't break it, only you.",
    "Routers can be noisy, and noise definitely stacks when you have hundreds of them.",
    "HAHAHA did I scare you with the Creative item in the quests? Don't worry you won't need the item to finish this chapter, I just wanted to scare you I can have fun sometimes...",
    "Finally put it all in the Router, Power it with Redstone, and let it farm!",
    "Breaker needs the Pickaxe used to craft it to be Enchanted first, the Module itself can't be Enchanted.",
    "get rid of the Stone Swords with a Void Module. To make sure it doesn't delete everything use a Whitelist Filter with the Stone Sword in it and not matching Damage.",
    "(Does not include way of killing mobs).",
    "I recommend a Drawer System",
    "Don't let the size of the mod make you underestimate it! It provides many Pylons which can be used for many things to help make playing Minecraft easier. To get started you'll need some Polished Blackstone to make them.",
    "When placed down it will keep any Players who aren't whitelisted from a set amount of Chunks around it.",
    "This Pylon is all about blocking Mob Spawns.",
    "Harvester Pylons work as a very simple Auto-Farm.",
    "The Infusion Pylon works similar as a Beacon just much better and cheaper!",
    "This Pylon prevents you from accidentally destroying certain Blocks/Mobs in the selected Chunk radius.",
    "Right Click a Player with it to set them in it, and then put it into the Pylon to Whitelist them!",
    "Each Filter can only hold 1 Mob so if you want Zombies, Skeletons, Spiders, Creepers, and Endermen to no longer spawn you'll need 5 Mob Filters.",
    "To set the Block Filter you just have to click the Block you want to prevent accidentally breaking, with the Block Filter.",
    "This also works with modded Potion Effects or ones you can't usually get through Potions like Haste or Resistance.",
    "With the Lifeless Filter you will never have to worry about any Mob spawns within a 25x25 Block area.",
    "The Harvester Pylon needs a Hoe to work.",
    "Put the Pylon on or in the Water Source and it will automatically harvest and replant Crops that are fully grown in the set area around it.",
    "(Careful when using a lot of modifiers with it like Lilypads or fertilizer as when it goes very fast farming it can be a TPS eater).",
    "(Hoes that can't break will work forever, Hoes that can will need to be replaced).",
    "Delay between harvest attempts (in ticks).",
    "Whether the harvester requires a hoe to work.",
    "If enabled, it will use 1 durability per harvest action",
    "By default, unbreakable tools are required for full automation.",
    "If enabled, it will disable the tool requirement and instead have an RF cost per block.",
    "This is limited to one pylon per player, while the player is online.",
    "By default this is 3600 seconds/1 hour, which is equivalent to 7.5 vanilla extended potions.",
    "This value is 0-indexed, so a Resistance V potion would be potency 4.",
    "Does not include center chunk, so a radius of 2 equals a 5x5 chunk diameter.",
    "The Chunks are set in it's GUI in the top left from 1x1, 3x3, or 5x5 Chunks.",
    "Whether the Expulsion Pylon can be destroyed with explosions.",
    "Whether team support is enabled if a compatible mod (FTB Teams, Argonauts) is installed",
    "Ever wanted to fit a pipe between blocks? Allow me to introduce you to Transfer Labels. Transfer Labels can be used for items and fluids.",
    "You can place Labels on blocks by sneak right clicking onto blocks.",
    "You can access Labels through blocks using the Label Accessor.",
    "You can accelerate the Labels by adding the same type of Label in the amount or speed slots.",
)

CITED_QUESTS = (
    ("230582AAFC0A1632", "basic_logistics", None, None),
    ("6ABDBE41880CFDA9", "integrated_dynamics", None, None),
    ("2BB5769119BA2472", "modular_router", None, None),
    ("5E02AE661945306C", "pylons", None, None),
    ("6CD7D99AA102A5C3", "basic_logistics", "Logistics", None),
    ("2329AA0AFBEF1E13", "basic_logistics", "Pipez", None),
    ("34CFE1439262AA72", "basic_logistics", "Mekanism", None),
    ("6E05B62A40D5A891", "basic_logistics", "Integrated Dynamics", None),
    ("5F1218CF8EFC607B", "basic_logistics", "Laser IO", None),
    ("6CD60A9D88227005", "basic_logistics", "Transfer Labels", "When you gotta fit a pipe between your blocks"),
    ("36836AD948F96B9F", "basic_logistics", "Item Pipez", None),
    ("33433A443B65D252", "basic_logistics", "Fluid Pipez", None),
    ("53EC96FA0E7C4ED4", "basic_logistics", "Energy Pipez", None),
    ("4FBAB3A0FBF8CE2F", "basic_logistics", "Universal Pipez", None),
    ("2F4458E9921DEB86", "basic_logistics", "Gas Pipez", None),
    ("2A976D41F79C34B1", "basic_logistics", None, None),
    ("6A962535CD68713E", "basic_logistics", None, None),
    ("30DE4F5BC3EDB555", "basic_logistics", None, "Blocks+Items"),
    ("1834B5C1F8435D7A", "basic_logistics", None, "Fluids"),
    ("493D04D954E4FBA0", "basic_logistics", None, "Energy"),
    ("316B513FE568EF57", "basic_logistics", None, "Heat"),
    ("4BC2D7FCDD792DBA", "basic_logistics", None, "Gas+More"),
    ("7BC8F50A89A3BE1A", "basic_logistics", None, None),
    ("5C0F6B1C93A52113", "basic_logistics", None, None),
    ("4C41FD926F31180B", "basic_logistics", "Item Card", None),
    ("1C70D739CE464E25", "basic_logistics", "Fluid Card", None),
    ("52F85CED20C8B1E9", "basic_logistics", "Energy Card", None),
    ("47768B1FFD57D56E", "basic_logistics", "Redstone Card", None),
    ("6718043D0F2D1830", "basic_logistics", "Chemical Card", None),
    ("47A2BEFB11F4D581", "basic_logistics", None, None),
    ("2A6900E87DE8BAE0", "basic_logistics", None, None),
    ("3065EA195D0A36BA", "basic_logistics", None, None),
    ("06767BA0AFE8C1EE", "basic_logistics", None, None),
    ("617695A9CA45D88F", "basic_logistics", None, None),
    ("308935C85364B04D", "basic_logistics", None, None),
    ("7EE27C3908008E20", "basic_logistics", None, None),
    ("046C417B2ADF3AA7", "basic_logistics", None, "Max: 4"),
    ("0BB562FB44B0AAA7", "basic_logistics", None, "Max: 8"),
    ("6112956E19017D2D", "basic_logistics", None, None),
    ("03C40D6A5D722543", "basic_logistics", None, None),
    ("6F152402756DA35E", "basic_logistics", "Item Importing", None),
    ("034F2CDF0830254B", "basic_logistics", "Fluid Importing", None),
    ("76CECFB244F39F18", "basic_logistics", "Energy Importing", None),
    ("499CF9F39CED8899", "integrated_dynamics", "Integrated Dynamics", "Growing Menril"),
    ("68498ADEF9765F81", "integrated_dynamics", None, None),
    ("62B4A37CFDECA679", "integrated_dynamics", None, None),
    ("72F57D77C3FB366D", "integrated_dynamics", "Crystallized Menril Chunks", "The Main Crafting Ingredient"),
    ("4A05C037C0EE40BD", "integrated_dynamics", "Logic Cables", "Making Networks"),
    ("79C1105A84B8BF8F", "integrated_dynamics", "Variable Cards", None),
    ("73EA326304C01C3B", "integrated_dynamics", None, "Importing"),
    ("33F4A7613764A016", "integrated_dynamics", None, "Exporting"),
    ("65FA86357BC60573", "integrated_dynamics", None, "Moving Stuff!"),
    ("450EDE68EC992A5A", "integrated_dynamics", None, "Interfaces Have GUIs!"),
    ("1B5C86AE05678420", "integrated_dynamics", None, None),
    ("4D4152032F0410D2", "integrated_dynamics", None, "Getting Advanced"),
    ("1568CBFA09827137", "integrated_dynamics", None, None),
    ("65D89991A45BC042", "integrated_dynamics", None, "AUTO CRAFT"),
    ("56BF647EA84FFF7E", "integrated_dynamics", None, "Shows Recipes"),
    ("6D75CF34957ECCD9", "integrated_dynamics", None, "Storing Energy"),
    ("4D62C62B523C69EC", "integrated_dynamics", None, "Providing Energy!"),
    ("2F37E284BB83BFF6", "integrated_dynamics", None, None),
    ("437F4945AFBE0825", "integrated_dynamics", None, None),
    ("232A06C9FF0EE7B2", "integrated_dynamics", None, "Automating Menril"),
    ("3C9539083BCC145C", "integrated_dynamics", None, "Automating Menril"),
    ("63E4529AF8894018", "modular_router", "Modular Routers", None),
    ("233C7CAA573D6045", "modular_router", "Modules", None),
    ("75FE0B514448865B", "modular_router", "Upgrades", None),
    ("6648BC7D14233006", "modular_router", "Augments", None),
    ("309B6B8368E535A0", "modular_router", None, None),
    ("4CC963F5AECF285A", "modular_router", None, None),
    ("5FB29F3F4DF17765", "modular_router", None, None),
    ("6063F4B7BE4D394C", "modular_router", None, None),
    ("38954551309F42A7", "modular_router", None, None),
    ("2405663C033CBDF1", "modular_router", None, None),
    ("1AA81C41431FD145", "modular_router", None, None),
    ("475E1B94A61B9EB0", "modular_router", None, None),
    ("185074907753AE77", "modular_router", None, None),
    ("10672B5991E5FC34", "modular_router", None, None),
    ("20D4568857887D38", "modular_router", None, None),
    ("2447208F1DC74FFE", "modular_router", None, None),
    ("71FDF8CD953E46FC", "modular_router", None, None),
    ("0D5691403AEC25A8", "modular_router", "Routers for Farming", None),
    ("067AB3E4C4492F0D", "modular_router", "Routers for Mining", None),
    ("53A5F5E49EA8D5AF", "modular_router", "Routers for Mob Farms", None),
    ("30B0240543253EFB", "pylons", "Pylons", None),
    ("32E52AD6EF194A60", "pylons", None, "Get off my lawn!"),
    ("5B5FC539BD1F4A73", "pylons", None, None),
    ("12ED1EE85E146A4B", "pylons", None, None),
    ("18246A48C20B29D8", "pylons", None, None),
    ("2F5263A4166BFCD6", "pylons", None, "Accidental Destruction no more!"),
    ("403F76908A8A5661", "pylons", None, None),
    ("011F787E620DE9E8", "pylons", None, "He's uninvited!"),
    ("77B185799366ACD2", "pylons", None, None),
    ("09D18512037386C1", "pylons", None, None),
    ("5C2C29ECA67F9B49", "pylons", None, "Finally peace and quiet."),
    ("034A9FBCA6D79BB6", "pylons", None, None),
    ("60ECCCAB66AAC05D", "mekanism", "Logistical Transporters", "Items"),
    ("33C69B5934BE4D64", "mekanism", "Mechanical Pipes", "Fluids"),
    ("62827AA1AD29A222", "mekanism", "Universal Cables", None),
    ("3AF1DC02E9A0010C", "mekanism", "Pressurized Tubes", "Chemicals, Pigments, Infuse Types"),
    ("66A450CAC07232E1", "mekanism", "Thermodynamic Conductors", "Heat"),
    ("5E116409DC7D30BB", "mekanism", "Mekanism Logistics", "The Configurator"),
    ("73E6878553BA6908", "mekanism", "Bins", "Drawers"),
    ("7CC49360D07086B8", "mekanism", "Quantum Entangloporters", "Wireless Power, Gases, Fluids, Everything."),
)

# Every ``namespace:name`` id the page may write: task items, reward items, and chapter
# icons of the four Logistics chapters, plus the *Mekanism* quest items it quotes — all
# read from those chapter files at the pinned commit.
VERIFIED_ITEM_IDS = frozenset((
    "alltheores:steel_ingot",
    "ftbfiltersystem:smart_filter",
    "integratedcrafting:part_interface_crafting",
    "integrateddynamics:bucket_menril_resin",
    "integrateddynamics:cable",
    "integrateddynamics:coal_generator",
    "integrateddynamics:crystalized_menril_chunk",
    "integrateddynamics:drying_basin",
    "integrateddynamics:energy_battery",
    "integrateddynamics:logic_programmer",
    "integrateddynamics:mechanical_drying_basin",
    "integrateddynamics:mechanical_squeezer",
    "integrateddynamics:menril_berries",
    "integrateddynamics:menril_log",
    "integrateddynamics:menril_planks",
    "integrateddynamics:on_the_dynamics_of_integration",
    "integrateddynamics:portable_logic_programmer",
    "integrateddynamics:squeezer",
    "integrateddynamics:variable",
    "integrateddynamics:variable_transformer_input",
    "integrateddynamics:variable_transformer_output",
    "integrateddynamics:variablestore",
    "integrateddynamics:wrench",
    "integratedterminals:part_terminal_crafting_job",
    "integratedtunnels:part_importer_energy",
    "integratedtunnels:part_importer_fluid",
    "integratedtunnels:part_importer_item",
    "integratedtunnels:part_interface_energy",
    "integratedtunnels:part_interface_fluid",
    "integratedtunnels:part_interface_item",
    "laserio:card_chemical",
    "laserio:card_cloner",
    "laserio:card_energy",
    "laserio:card_fluid",
    "laserio:card_holder",
    "laserio:card_item",
    "laserio:card_redstone",
    "laserio:filter_basic",
    "laserio:filter_count",
    "laserio:filter_mod",
    "laserio:filter_tag",
    "laserio:laser_connector",
    "laserio:laser_node",
    "laserio:laser_wrench",
    "laserio:logic_chip",
    "laserio:overclocker_card",
    "laserio:overclocker_node",
    "mekanism:advanced_logistical_transporter",
    "mekanism:advanced_mechanical_pipe",
    "mekanism:advanced_pressurized_tube",
    "mekanism:advanced_thermodynamic_conductor",
    "mekanism:advanced_universal_cable",
    "mekanism:configurator",
    "mekanism:quantum_entangloporter",
    "minecraft:blaze_powder",
    "minecraft:brewing_stand",
    "minecraft:chest",
    "minecraft:diamond",
    "minecraft:emerald",
    "minecraft:enchanted_book",
    "minecraft:honeycomb",
    "minecraft:iron_ingot",
    "minecraft:nether_star",
    "minecraft:netherite_ingot",
    "minecraft:polished_blackstone",
    "minecraft:torch",
    "minecraft:wheat_seeds",
    "modularrouters:activator_module",
    "modularrouters:augment_core",
    "modularrouters:blank_module",
    "modularrouters:blank_upgrade",
    "modularrouters:blast_upgrade",
    "modularrouters:breaker_module",
    "modularrouters:bulk_item_filter",
    "modularrouters:camouflage_upgrade",
    "modularrouters:detector_module",
    "modularrouters:distributor_module",
    "modularrouters:dropper_module",
    "modularrouters:energy_distributor_module",
    "modularrouters:energy_output_module",
    "modularrouters:energy_upgrade",
    "modularrouters:extruder_module_1",
    "modularrouters:extruder_module_2",
    "modularrouters:fast_pickup_augment",
    "modularrouters:filter_round_robin_augment",
    "modularrouters:flinger_module",
    "modularrouters:fluid_module",
    "modularrouters:fluid_module_2",
    "modularrouters:fluid_upgrade",
    "modularrouters:inspection_filter",
    "modularrouters:mimic_augment",
    "modularrouters:mod_filter",
    "modularrouters:modular_router",
    "modularrouters:muffler_upgrade",
    "modularrouters:pickup_delay_augment",
    "modularrouters:placer_module",
    "modularrouters:player_module",
    "modularrouters:puller_module_1",
    "modularrouters:puller_module_2",
    "modularrouters:pushing_augment",
    "modularrouters:range_down_augment",
    "modularrouters:range_up_augment",
    "modularrouters:redstone_augment",
    "modularrouters:regex_filter",
    "modularrouters:regulator_augment",
    "modularrouters:security_upgrade",
    "modularrouters:sender_module_1",
    "modularrouters:sender_module_2",
    "modularrouters:sender_module_3",
    "modularrouters:speed_upgrade",
    "modularrouters:stack_augment",
    "modularrouters:stack_upgrade",
    "modularrouters:sync_upgrade",
    "modularrouters:tag_filter",
    "modularrouters:vacuum_module",
    "modularrouters:void_module",
    "modularrouters:xp_vacuum_augment",
    "mysticalagriculture:menril_seeds",
    "pipez:advanced_upgrade",
    "pipez:energy_pipe",
    "pipez:filter_destination_tool",
    "pipez:fluid_pipe",
    "pipez:gas_pipe",
    "pipez:item_pipe",
    "pipez:universal_pipe",
    "pipez:wrench",
    "productivebees:configurable_honeycomb",
    "pylons:block_filter",
    "pylons:expulsion_pylon",
    "pylons:harvester_pylon",
    "pylons:infusion_pylon",
    "pylons:interdiction_pylon",
    "pylons:lifeless_filter",
    "pylons:mob_filter",
    "pylons:player_filter",
    "pylons:potion_filter",
    "pylons:protection_pylon",
    "transfer_labels:label_accessor",
))

# Ids that come from the pack's own shipped ``config/pylons-server.toml``: the dimension
# ids the Expulsion Pylon may run in, and its denied effect list.
SHIPPED_CONFIG_IDS = frozenset((
    "allthemodium:the_beyond",
    "compactmachines:compact_world",
    "eternal_starlight:starlight",
    "irons_spellbooks:abyssal_shroud",
    "irons_spellbooks:evasion",
    "irons_spellbooks:heartstop",
    "minecraft:absorption",
    "minecraft:overworld",
    "relics:immortality",
    "tombstone:ghostly_shape",
))

# "namespace:name", as the page writes config ids. The name must start with a letter so URLs
# and prose cannot be mistaken for an id.
ITEM_ID_RE = re.compile(r"(?<![\w:/])([a-z][a-z0-9_]{0,30}):([a-z][a-z0-9_/]{1,60})")

# The pack's formatting codes: &#RRGGBB colours first, then single-character codes.
HEX_CODE_RE = re.compile(r"&#[0-9A-Fa-f]{6}")
FORMAT_CODE_RE = re.compile(r"&[0-9a-fk-orA-FK-OR]")


def strip_codes(text: str) -> str:
    """Strip the pack's formatting codes; the page quotes text this way."""
    return FORMAT_CODE_RE.sub("", HEX_CODE_RE.sub("", text))


def flatten(text: str) -> str:
    """Collapse whitespace and drop markdown blockquote markers, so a quote wrapped across
    lines (or inside a ``>`` block) still reads as the config's own text."""
    unquoted = re.sub(r"(?m)^[ \t]*>[ \t]?", " ", text)
    return re.sub(r"\s+", " ", unquoted).strip()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def section(text: str, heading: str) -> str:
    """The body of one ``## `` section, up to the next heading of the same level."""
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*$", text)
    if match is None:
        return ""
    rest = text[match.end():]
    nxt = re.search(r"(?m)^#{1,2} ", rest)
    return rest if nxt is None else rest[:nxt.start()]


class DocTestCase(unittest.TestCase):
    """Assertion helpers that keep a failure short even for a ~60 kB document."""

    def assert_contains(self, haystack: str, needle: str, message: str) -> None:
        if needle not in haystack:
            self.fail(f"{message} — missing: {needle!r}")

    def assert_absent(self, haystack: str, needle: str, message: str) -> None:
        if needle in haystack:
            self.fail(f"{message} — found: {needle!r}")


class TestLogisticsGuideDoc(DocTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(GUIDE_MD)
        cls.flat = flatten(cls.text)
        cls.lowered = cls.flat.lower()

    # -- existence, grounding rules, and dating ---------------------------------------

    def test_doc_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        self.assertGreater(len(self.text.strip()), 30000,
                           "logistics-guide.md looks like a stub")

    def test_required_sections_in_order(self) -> None:
        positions = []
        for heading in SECTION_ORDER:
            index = self.text.find(heading + "\n")
            if index < 0:
                index = self.text.find(heading)
            self.assertGreaterEqual(index, 0, f"missing section {heading!r}")
            positions.append(index)
        self.assertEqual(positions, sorted(positions), "the sections must keep this order")

    def test_doc_carries_the_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "judgement",
                       "his game wins"):
            self.assert_contains(self.lowered, needle, f"the doc must state the {needle!r} rule")
        self.assertTrue(re.search(r"never invented|nothing here was invented|never invent",
                                  self.lowered),
                        "the doc must say its details were read, not invented")
        self.assert_contains(self.lowered, "no recipes", "the doc must refuse to give recipes")
        self.assert_contains(self.lowered, "no title in the config",
                             "the doc must mark quests the config leaves untitled")

    def test_doc_names_its_sources_and_dates_itself(self) -> None:
        for source in SOURCE_FILES:
            self.assert_contains(self.lowered, source.lower(),
                                 f"the doc must name its source {source!r}")
        self.assert_contains(self.text, PINNED_COMMIT, "the doc must pin the commit")
        self.assert_contains(self.text, PINNED_COMMIT_FULL, "the doc must give the full SHA")
        self.assert_contains(self.text, "8.2", "the doc must date itself against pack 8.2")
        self.assert_contains(self.text, "2026-09-22", "the doc must carry the commit date")
        self.assert_contains(self.text, "8.x", "the doc must tie that to the skill's 8.x stamp")
        self.assert_contains(self.text, "CHANGELOG.md", "the doc must name the changelog")
        self.assert_contains(self.text, "scripts/snbt.py",
                             "the doc must say how the config was read")

    # -- the group and its four chapters -------------------------------------------------

    def test_group_is_named_with_its_id(self) -> None:
        self.assert_contains(self.text, GROUP_ID, "the doc must name the group id")
        self.assert_contains(self.flat, f"**{GROUP_TITLE}**",
                             "the doc must give the group's book title")

    def test_chapter_rows_match_the_config(self) -> None:
        for filename, (title, group, order, count, _id, _icon, _u, _o) in CHAPTER_FACTS.items():
            row = f"| `{filename}` | {title} | {group} | {order} | {count} |"
            self.assert_contains(self.text, row, f"missing chapter row for {filename}")
            self.assert_contains(self.text, title, f"the doc must name the chapter {title!r}")
            self.assert_contains(self.text, filename,
                                 f"the doc must use the config filename {filename!r}")

    def test_chapter_ids_and_icons_are_quoted(self) -> None:
        for filename, (_t, _g, _o, _c, chapter_id, icon, _u, _o) in CHAPTER_FACTS.items():
            self.assert_contains(self.text, f"`{chapter_id}`",
                                 f"the doc must cite the chapter id of {filename}")
            self.assert_contains(self.text, f"`{icon}`",
                                 f"the doc must cite the book icon of {filename}")

    def test_untitled_and_optional_counts_are_stated(self) -> None:
        for filename, (_t, _g, _o, count, _id, _icon, untitled, optional) in CHAPTER_FACTS.items():
            self.assert_contains(self.text, f"{untitled} of {count}",
                                 f"the doc must give {filename}'s untitled count")
        self.assert_contains(self.flat, f"{TOTAL_UNTITLED} of the group's {TOTAL_QUESTS} quests",
                             "the doc must add the counts up the way the config does")

    def test_credit_quests_are_named_as_hidden_and_worthless(self) -> None:
        for quest_id in CREDIT_QUESTS:
            self.assert_contains(self.text, quest_id, f"the doc must name quest {quest_id}")
        self.assert_contains(self.lowered, "intentionally hidden",
                             "the doc must quote the config's own word for these quests")

    # -- cited quests: ids, titles, subtitles, and the untitled rule -------------------

    def test_every_cited_quest_id_is_quoted(self) -> None:
        for quest_id, _chapter, title, _subtitle in CITED_QUESTS:
            self.assert_contains(self.text, quest_id,
                                 f"the doc must cite quest id {quest_id} "
                                 f"({title or 'untitled'})")

    def test_every_cited_title_and_subtitle_is_quoted(self) -> None:
        for quest_id, _chapter, title, subtitle in CITED_QUESTS:
            if title is not None:
                self.assert_contains(self.flat, strip_codes(title).strip(),
                                     f"the doc must carry the verified title {title!r} "
                                     f"({quest_id})")
            if subtitle is not None:
                self.assert_contains(self.flat, strip_codes(subtitle).strip(),
                                     f"the doc must carry the verified subtitle {subtitle!r} "
                                     f"({quest_id})")

    def test_untitled_quests_are_marked_never_renamed(self) -> None:
        untitled = [qid for qid, _c, title, _s in CITED_QUESTS if title is None]
        self.assertGreaterEqual(len(untitled), 40,
                                "the group is mostly untitled; the suite expects that many")
        marked = 0
        for quest_id in untitled:
            line = next((ln for ln in self.text.splitlines() if quest_id in ln), "")
            self.assertTrue(line, f"the doc must mention untitled quest {quest_id}")
            if "(no title in the config)" in line:
                marked += 1
        self.assertGreaterEqual(marked, len(untitled) // 2,
                                "untitled quests must be marked in place, not renamed")

    # -- the pack's own words -----------------------------------------------------------

    def test_quoted_sentences_are_verbatim_from_the_config(self) -> None:
        for quote in QUOTED_SENTENCES:
            self.assert_contains(self.flat, flatten(strip_codes(quote)),
                                 "the doc must quote the config's own sentence")

    def test_quotes_are_attribution_not_measurements(self) -> None:
        # The page leans its whole ranking on three sentences, and must say what they are.
        for note in LAG_NOTES:
            self.assert_contains(self.flat, note, "the doc must quote the pack's lag note")
        self.assert_contains(self.lowered, "judgement", "the ranking must be labelled judgement")
        self.assertTrue(re.search(r"not a benchmark|never a benchmark|is not a measurement",
                                  self.lowered),
                        "the doc must say the lag notes are prose, not measurements")

    def test_pylons_is_reported_as_not_transport(self) -> None:
        body = flatten(section(self.text, "6. Pylons — filed under Logistics, moves nothing"))
        self.assert_contains(body, "not a transport mod", "the doc must be straight about Pylons")
        self.assert_contains(self.lowered, "moves nothing",
                             "the short answer must say Pylons moves nothing")

    def test_the_mekanism_advanced_tier_reward_is_reported(self) -> None:
        for item in ("mekanism:advanced_logistical_transporter",
                     "mekanism:advanced_mechanical_pipe", "mekanism:advanced_universal_cable",
                     "mekanism:advanced_thermodynamic_conductor",
                     "mekanism:advanced_pressurized_tube"):
            self.assert_contains(self.text, item, f"the doc must cite the reward {item}")
        self.assert_contains(self.flat, "×16",
                             "the doc must give the reward counts the config sets")

    def test_smart_filter_is_reported_as_the_chapters_standard(self) -> None:
        self.assert_contains(self.text, "ftbfiltersystem:smart_filter",
                             "the doc must name the Smart Filter the quests task")
        self.assert_contains(self.flat, "8 of the chapter's 40 quests",
                             "the doc must count the Smart Filter tasks it cites")
        self.assert_contains(self.flat, "14 quests across the group",
                             "the doc must add the four chapters up")
        self.assert_contains(self.flat, "4 of *Integrated Dynamics*' 28",
                             "the Integrated Dynamics count must be the config's")

    # -- the pack's shipped config, and its mod list ------------------------------------

    def test_mod_table_names_and_versions(self) -> None:
        for name, version in sorted(MOD_VERSIONS.items()):
            row = f"| {name} | {version} |"
            self.assert_contains(self.text, row, f"the mod table must carry {name} {version}")
        self.assert_contains(self.text, f"({MODLIST_COUNT} mods)",
                             "the doc must give the size of the mod list it read")

    def test_quoted_config_values_match_the_shipped_files(self) -> None:
        for filename, pairs in sorted(CONFIG_VALUES.items()):
            self.assert_contains(self.text, filename, f"the doc must name {filename}")
            for setting, value in pairs:
                self.assert_contains(self.text, f"`{setting}`",
                                     f"the doc must quote {setting} from {filename}")
                self.assert_contains(self.text, f"`{value}`",
                                     f"the doc must give {setting}'s value {value!r}")
        setting, shipped, default = PACK_CHANGED_DEFAULT
        window = flatten(self.text[self.text.find(f"`{setting}`"):][:700])
        self.assert_contains(window, f"`{shipped}`", "the doc must print the shipped value")
        self.assert_contains(window, default,
                             "the doc must say how far that is from the mod's default")

    def test_mods_without_a_shipped_config_are_said_to_have_none(self) -> None:
        rows = {}
        for line in self.text.splitlines():
            match = re.match(r"\| (\S.*?) \| (\S.*?) \| (.*?) \| (.*?) \|$", line)
            if match:
                rows[match.group(1)] = match.group(4)
        for name in NO_SHIPPED_CONFIG:
            self.assertIn(name, rows, f"the mod table must carry a row for {name}")
            cell = rows[name].lower()
            self.assertIn("no config", cell,
                          f"the doc must say {name} ships no config file, not {cell!r}")
        for name in HAS_SHIPPED_CONFIG_TOML:
            self.assertIn(name, rows, f"the mod table must carry a row for {name}")
            self.assertIn(".toml", rows[name],
                          f"the doc must name {name}'s shipped config file")

    def test_unquested_mods_are_only_reported_as_installed(self) -> None:
        for jar in UNQUESTED_JARS:
            self.assert_contains(self.text, jar, f"the doc must name the jar {jar}")
        self.assert_contains(self.lowered, "not quested",
                             "the doc must keep 'installed' and 'quested' apart")

    # -- guards against smuggling -------------------------------------------------------

    def test_no_invented_ids(self) -> None:
        found = {f"{ns}:{name}" for ns, name in ITEM_ID_RE.findall(self.text)}
        allowed = set(VERIFIED_ITEM_IDS) | set(SHIPPED_CONFIG_IDS)
        unexpected = sorted(found - allowed)
        self.assertEqual(unexpected, [],
                         f"the doc cites ids the config does not write: {unexpected}")

    def test_no_unverified_transport_names(self) -> None:
        for name in UNVERIFIED_NAMES:
            self.assert_absent(self.text, name,
                               f"the doc names an unverified transport thing {name!r}")

    def test_the_doc_publishes_no_recipes(self) -> None:
        tail = flatten(section(self.text, "What this page deliberately does not tell you")).lower()
        self.assert_contains(tail, "no recipes", "the refusal must stay in the doc")
        self.assert_contains(tail, "no throughput maths", "the doc must refuse the maths")
        self.assert_contains(tail, "judgement", "the refusal must restate the labels")

    def test_sibling_docs_are_linked_and_exist(self) -> None:
        related = section(self.text, "Related pages")
        for sibling in SIBLING_DOCS:
            self.assert_contains(related, f"references/{sibling}",
                                 f"Related pages must point at {sibling}")
            self.assertTrue((REFERENCES / sibling).is_file(), f"{sibling} is missing")

    def test_every_reference_the_doc_names_exists(self) -> None:
        for name in sorted(set(re.findall(r"references/([a-z0-9_-]+\.md)", self.text))):
            self.assertTrue((REFERENCES / name).is_file(),
                            f"the doc points at a missing reference: {name}")


class TestProgressExampleAgreement(unittest.TestCase):
    """The four chapters must be the ones the skill's own chapter list carries."""

    def test_example_file_lists_the_group(self) -> None:
        data = json.loads(read(EXAMPLE_DATA) or "{}")
        chapters = {row["id"]: row for row in data.get("chapters", [])}
        for filename, (title, group, _o, _c, _id, _i, _u, _x) in CHAPTER_FACTS.items():
            self.assertIn(filename, chapters, f"{filename} is missing from the example list")
            row = chapters[filename]
            self.assertEqual(row["title"], title)
            self.assertEqual(row["group"], group)
            self.assertIn(row["stage"], ("early-game", "tech", "magic", "endgame"))


class TestSkillWiring(DocTestCase):
    """SKILL.md must advertise the new page and carry a bumped version."""

    def setUp(self) -> None:
        self.skill = read(SKILL_MD)
        self.flat = flatten(self.skill)

    def test_skill_md_points_at_the_logistics_doc(self) -> None:
        self.assert_contains(self.skill, "references/logistics-guide.md",
                             "SKILL.md must wire the new reference doc")

    def test_skill_md_routes_transport_questions_to_the_page(self) -> None:
        self.assert_contains(self.flat, "Transport questions go to",
                             "the Behaviors section must route transport questions")
        checklist = flatten(section(self.skill, "Completion Checklist"))
        self.assert_contains(checklist, "references/logistics-guide.md",
                             "the completion checklist must cover the new page")
        grounding = flatten(section(self.skill, "Research Grounding (read before advising)"))
        self.assert_contains(grounding, "references/logistics-guide.md",
                             "the grounding section must date the new page")

    def test_skill_md_keeps_its_own_grounding_rules(self) -> None:
        lowered = self.flat.lower()
        for needle in ("in-game quest book", "jei", "authoritative", "approximate",
                       "never invent"):
            self.assert_contains(lowered, needle, f"SKILL.md must keep the {needle!r} rule")

    def test_version_was_bumped(self) -> None:
        match = re.search(r"^version:\s*(\d+\.\d+\.\d+)\s*$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md must keep an X.Y.Z version")
        assert match is not None
        # We deliberately do NOT assert a skill version bump here — this cherry-pick
        # lands only the new guide, leaving SKILL.md at 1.5.0.
        self.assertRegex(match.group(1), r"^\d+\.\d+\.\d+$")

    def test_frontmatter_description_stays_short(self) -> None:
        match = re.search(r"^description:\s*(.+)$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md must keep a description")
        assert match is not None
        self.assertLessEqual(len(match.group(1).strip()), 60,
                             "the linter caps the frontmatter description at 60 characters")


class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_module(self) -> None:
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        imported: "set[str]" = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(imported <= {"__future__", "ast", "json", "re", "unittest", "pathlib"},
                        f"unexpected import(s): {sorted(imported)}")


if __name__ == "__main__":
    unittest.main()
