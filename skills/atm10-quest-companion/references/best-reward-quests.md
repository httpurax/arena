# Best reward quests — a high-value pick list (verified rewards)

**What this page is.** A short answer to “which quests are worth doing for their
rewards?” in **All the Mods 10**, not a completion checklist or a crafting guide.
**Beginner answer (judgement):** inspect **Charging Gadgets**, the three **Item Pipez** /
**Fluid Pipez** / **Energy Pipez** entries, **Tool Belt**, and the storage rebates first.
Claim **Welcome to Getting Started!** along the way. Then collect the progression
rebates on the route you actually want to play; do not rush bosses or post-star quests
solely because their reward looks large.

## Provenance — read from the pinned pack config

Only the official [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) repository
at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
is used here. Its `CHANGELOG.md` identifies **pack 8.2**, dated **2026-09-22**.
Nothing below is sourced from community advice or mod mechanics remembered from elsewhere.

- `config/ftbquests/quests/chapters/<chapter>.snbt`: quest ids, tasks, dependencies,
  fixed item rewards and their counts/components, plus other reward types.
- `config/ftbquests/quests/lang/en_us/chapters/<chapter>.snbt`: explicit English quest
  titles and descriptions; `lang/en_us/chapter.snbt`: chapter titles. Paths are relative
  to `config/ftbquests/quests/` for the language files.
- The table's chapter keys are the exact config filenames without `.snbt`.
  The corresponding config and language files share that key. This makes every entry
  auditable at the pinned commit without guessing from an item display name.
- `tests/fixtures/best_reward_quests.json` preserves a small reviewed extraction of the
  listed quests' tasks, dependencies, full rewards, raw titles and descriptions at this
  snapshot. It is for offline regression checks, not a replacement quest book.

## Grounding rules — facts versus value judgements

- **The in-game quest book (FTB Quests) is authoritative.** If it differs from this
  snapshot, trust the book and say so. Use JEI for current recipes and item behaviour.
- **Every named quest title below is quoted from the config**, with Minecraft colour
  and style codes removed only. A quest with no explicit title is marked as such;
  never promote its task item's name into a verified quest title.
- **All priority order, “worth it” reasoning, and beginner/later groupings are judgement
  (approximate)**, not a pack-defined ranking or guaranteed time saving. There is no
  measured cost/benefit ratio here. A reward may be valuable only on your chosen route.
- The payoff column quotes **fixed `item` rewards only**, including stored components
  where present. It is not the complete reward list: XP and table-based bonuses are
  omitted. `×N` is the reward's explicit count, or the item stack's count when no
  reward-level count is set. Components are config data, not an inferred effect.
- A reward is **not** a task, recipe, drop, or unlock. Check all dependencies and task
  filters in the book first. An extra copy of a task item is usually a rebate, not a
  way to acquire your first copy. No crafting gates or cross-mod bridges are inferred.
- No recipes, coordinates, dimension routes, or invented requirement counts are supplied.

## The pick list

Each “Why inspect it?” cell is **judgement (approximate)**. Ids distinguish similarly
named quests. The tables are advice order, not quest-book or dependency order.

### Finding the chapters in the book (verified chapter titles)

- `mainquestline_part_1` → **Chapter 1: The Beginning**.
- `tips_and_tricks` → **Tips and Tricks**.
- `basic_logistics` → **Basic Logistics**.
- `storage` → **Basic Storage**.
- `allthemodium` → **Chapter 2: Allthemodium**.
- `powah` → **Powah**.
- `iron_spells_and_spellbooks` → **Iron's Spells 'n Spellbooks**.
- `deeper_and_darker` → **Deeper and Darker**.
- `aether` → **The Aether**.
- `achapter_2r_6the_atm_star` → **Chapter 4: Creative**.

### Check first — beginner-friendly priorities (judgement)

| Chapter key | Verified quest title | Quest id | Fixed payoff in config | Why inspect it? (judgement) |
|---|---|---|---|---|
| `mainquestline_part_1` | **Welcome to Getting Started!** | `5CF320E9C4C1B1E1` | `minecraft:torch` ×4<br>`minecraft:cooked_beef` ×4 | Small but useful starter supplies; claim while getting started. |
| `tips_and_tricks` | **Charging Gadgets** | `637981B64BBE0D92` | `mekanism:basic_energy_cube` ×1; components: `{"mekanism:energy":{"energy_containers":[4000000]}}` | A configured energy-bearing cube makes this my first tech detour to inspect. |
| `tips_and_tricks` | **Tool Belt** | `378C95C18798D413` | `toolbelt:pouch` ×2 | Worth checking if you already use a belt; its description says pouches increase capacity. |
| `basic_logistics` | **Item Pipez** | `36836AD948F96B9F` | `pipez:item_pipe` ×16 | Extra pipes for an item-moving setup you were building anyway. |
| `basic_logistics` | **Fluid Pipez** | `33433A443B65D252` | `pipez:fluid_pipe` ×16 | Extra pipes if your setup moves fluids. |
| `basic_logistics` | **Energy Pipez** | `53EC96FA0E7C4ED4` | `pipez:energy_pipe` ×16 | Extra pipes if your setup moves energy. |
| `storage` | **Iron Chest** | `58514FDE153FD971` | `sophisticatedstorage:basic_to_iron_tier_upgrade` ×1 | An extra tier upgrade when you are already upgrading storage. |
| `storage` | **Gold Chest** | `3E33730DC2115D26` | `sophisticatedstorage:iron_to_gold_tier_upgrade` ×1 | Another storage-upgrade rebate; do not build the whole chain just for this. |
| `storage` | **Copper Upgrade** | `485D5664A17E16DF` | `functionalstorage:copper_upgrade` ×1 | An extra drawer upgrade if you are choosing this storage route. |

### Progression rebates — claim when you get there (judgement)

| Chapter key | Verified quest title | Quest id | Fixed payoff in config | Why inspect it? (judgement) |
|---|---|---|---|---|
| `mainquestline_part_1` | **Netherite Template** | `1E1EB7DC19DDCFB7` | `minecraft:netherite_upgrade_smithing_template` ×1 | An additional template after acquiring the task item; not a free first template. |
| `mainquestline_part_1` | **Summoning The Wither** | `4A4C71C43519D5FE` | `minecraft:wither_skeleton_skull` ×3 | A skull rebate once the listed skull and soul-sand tasks are met; not a boss kill reward. |
| `allthemodium` | **Allthemodium Ingot** | `201EE3566D4D3123` | `allthemodium:allthemodium_ingot` ×1 | An extra ingot after obtaining the task ingot and meeting dependencies. |
| `allthemodium` | **Teleport Pad** | `07FDA46D83F8360D` | `allthemodium:allthemodium_nugget` ×4 | A nugget rebate when you already have the pad; no recipe shortcut implied. |
| `storage` | **Netherite Backpack** | `46D756F4DC6CC894` | `minecraft:netherite_ingot` ×1 | An ingot rebate for a backpack you already wanted; not a reason to rush the tier. |
| `powah` | **Welcome to Powah!!!** | `6B2027DA7AA6FF34` | `powah:book` ×1<br>`powah:wrench` ×1 | Useful starter accessories if you are committing to this tech chapter. |

### Magic / exploration payoffs — only on your chosen route (judgement)

| Chapter key | Verified quest title | Quest id | Fixed payoff in config | Why inspect it? (judgement) |
|---|---|---|---|---|
| `iron_spells_and_spellbooks` | **Legendary Ink** | `67D40A1A9332C03D` | `irons_spellbooks:legendary_ink` ×2 | Extra ink after obtaining the task ink; a rebate rather than a first-ink source. |
| `iron_spells_and_spellbooks` | **Ancient Codex** | `7408CCF998D9CD37` | `irons_spellbooks:legendary_ink` ×1 | Ink alongside your spell-book progression; check the actual task, not just the title. |
| `iron_spells_and_spellbooks` | **Allthemodium Spell Book** | `445C21949ADA1FE3` | `allthemodium:allthemodium_upgrade_smithing_template` ×1 | A template rebate for an existing spell-book goal, not a free first book. |
| `deeper_and_darker` | **Soul Elytra** | `4A01C5F5DCF32C19` | `minecraft:enchanted_book` ×1; components: `{"minecraft:stored_enchantments":{"levels":{"minecraft:mending":1}}}` | A specifically configured enchanted book; inspect if you already pursue this quest. |
| `aether` | **Valkyrie Queen** | `0D2F07FC0F804223` | `aether:valkyrie_helmet` ×1<br>`aether:valkyrie_chestplate` ×1<br>`aether:valkyrie_leggings` ×1<br>`aether:valkyrie_boots` ×1 | A full set of listed armor rewards; a route-specific payoff, not a beginner boss recommendation. |

### Post-star payoffs — not beginner detours (judgement)

| Chapter key | Verified quest title | Quest id | Fixed payoff in config | Why inspect it? (judgement) |
|---|---|---|---|---|
| `achapter_2r_6the_atm_star` | **Star Shards** | `73201E591C2A40CC` | `allthetweaks:atm_star_shard` ×10 | A shard rebate, but the quest has dependencies; possessing a shard alone is not enough. |
| `achapter_2r_6the_atm_star` | **Fully Automated ATM Star** | `5436157FDFC9633E` | `allthetweaks:atm_star_shard` ×50<br>`allthetweaks:patrick_star` ×1 | Large shard reward on a dependency-heavy terminal quest; no free ATM Star is promised. |

For the post-star dependency map rather than reward shopping, read
`references/creative-checklist.md`. Those rewards are not evidence that the pack gives
away creative items or automates the star merely by claiming a quest.

## Useful unnamed entry — do not invent a title

| Chapter key | Verified quest title | Quest id | Fixed payoff in config | Why inspect it? (judgement) |
|---|---|---|---|---|
| `basic_logistics` | *(no explicit title in config)* | `2A976D41F79C34B1` | `pipez:advanced_upgrade` ×1 | An upgrade rebate to inspect if already using Pipez. |

This quest's task item is `pipez:filter_destination_tool`; that is a **task item id**,
not a quest title or a reward. The book supplies the displayed name; use the id to
locate the entry if needed.

## Reward traps and uncertainties

- **Kill The Warden** (`mainquestline_part_1`, `6D09511D64DDC282`) rewards
  `minecraft:potion` ×1 with component
  `{"minecraft:potion_contents":{"potion":"potionsmaster:allthemodium"}}`, plus XP.
  **It does not reward an Allthemodium ingot in this snapshot.** The config alone does
  not establish the potion's effect or duration. Judgement: do not take on this fight
  just for an assumed ingot; inspect your book before making the detour.
- **Charging Gadgets** has a fixed cube **and** a `random` table reward. Its random
  reward has `exclude_from_claim_all: true`; the cube's energy component is shown
  verbatim above, with no inferred unit, charging compatibility, or runtime promised.
- Table rewards are not fixed item promises. For example, **The Metal Age**
  (`mainquestline_part_1`, `051E0C85E7B71CE0`) has a `loot` reward with
  `exclude_from_claim_all: true`. **We've Struck Diamonds!**
  (`mainquestline_part_1`, `76406EFFF8CBA6B4`) likewise has a `loot` reward with that flag.
  Judgement: inspect these bonuses when completing the normal starter route, but do
  not pursue them expecting a particular rare item. This page does not evaluate their
  reward-table contents or claim odds; check the book's current reward interface.
- Do not assume Claim All handles every bonus: where the config excludes a reward,
  inspect that reward individually. Whether a quest is currently claimable depends on
  your book and progress; this page neither grants rewards nor records completion.

## How to answer the beginner in practice (judgement)

Offer a few relevant entries, not the entire table: name the exact title, its chapter
key, the fixed payoff, and why it fits what the player is already building. Ask them to
open that entry, meet its dependencies/tasks, and inspect the reward before spending
resources. If they ask for crafting details or item effects not quoted here, say
“check the quest entry / JEI” instead of filling gaps from memory.
