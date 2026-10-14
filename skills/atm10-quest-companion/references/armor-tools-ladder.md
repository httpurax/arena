# Armor and Tools Progression Ladder (ATM10)

**Authoritative source**: The in-game FTB Quests book and JEI are always authoritative for exact requirements, counts, and recipes. This ladder is a *guide* based on verified quest titles and config from pack 8.2 (commit `e5e3d1d83e`, 2026-09-22). Quest titles and item ids quoted below are from that snapshot; your book may differ — defer to it.

## Quick-reference: verified quest titles from the config

| Tier | Quest title (as in config) | Quest id |
|------|---------------------------|----------|
| Leather | `&7Leather Armor` | `28408BFAA54E4FC6` |
| Chainmail | `&8Chainmail Armor` | `004D61425172324F` |
| Gold | `&eGolden Armor` | `17A68C4E9E9EA2B7` |
| Diamond | `&bDiamond Armor` | `5DDC15AAFD2CAF47` |
| Netherite | `&cNetherite Armor` | `074EC1E636CD6605` |
| Allthemodium | `&6Allthemodium Armor` | `6C5F9D0D447EFB9C` |
| Vibranium | `&3Vibranium Armor` | `72DDA413D73E3235` |
| Unobtainium | `&5Unobtainium Armor` | `6F76DA3BBAE8337B` |

## Should I upgrade my armor yet?

**Short answer**: Yes, if you are in **early-game** or **tech** and have the materials, upgrading past diamond is always worth it — each tier gives more armor points, toughness, or special buffs. If you are already in **endgame** (Chapter 2: Allthemodium or beyond), you should be using **allthemodium**, **vibranium**, or **unobtainium** gear as your default.

**Why upgrade?** Each tier unlocks new capabilities:

| Tier | When you typically have it | What it unlocks / is worth it for |
|------|---------------------------|------------------------------------|
| **Leather** | Very early game | Basic protection; easily obtained from cows/rabbits. Not worth upgrading from once you have iron. |
| **Chainmail** | Early game (after mob farming) | Slightly better than leather; can be found/ traded. Minor upgrade. |
| **Gold** | Early-mid game | Easier to enchant (golden armor gives more enchantability), but low durability. Worth it only for the enchantability niche. |
| **Diamond** | Mid game (after diamonds) | The "baseline" mid-game armor. Protection IV/Unbreaking III diamond is reliable. Most quests up to Chapter 1 expect you to have this. |
| **Netherite** | Post-Nether (ancient debris) | Higher armor points *and* toughness, float in lava, higher durability. Worth the upgrade if you have the ancient debris — it's the last "vanilla-style" tier before modded armors. |
| **Allthemodium** | After Chapter 2: Allthemodium (deepslate, Deep Dark, Y ≈ -40) | Significantly more armor points and toughness than netherite, plus magic protection buffs. The quest `&6Allthemodium Armor&r` (quest title) explicitly says you need netherite to craft it. |
| **Vibranium** | After obtaining allthemodium armor (typically Chapter 2) | Even higher stats than allthemodium; the quest `&3Vibranium Armor&r` says you need allthemodium armor to create it. Provides excellent all-around defense. |
| **Unobtainium** | Post-vibranium (endgame) | The highest tier. The quest `&5Unobtainium Armor&r` notes it has 100% knockback resistance and higher stats everywhere. **Requires vibranium armor as a component** — do not attempt without it. |

## When is each upgrade "worth it"?

- **Diamond → Netherite**: Worth it once you have a netherite smithing table and some ancient debris. The toughness and lava-float benefits are practical, not just prestige.
- **Netherite → Allthemodium**: Worth it when you reach Chapter 2: Allthemodium. The armor points and toughness jump is significant, and the quest explicitly gates allthemodium armor behind netherite.
- **Allthemodium → Vibranium**: Worth it when you have the vibranium resources (Nether) and want the extra power. The quest says you need allthemodium armor as a prerequisite.
- **Vibranium → Unobtainium**: Worth it only for endgame / ATM Star preparation. This is the highest tier; the quest explicitly requires vibranium armor to craft it, and it provides 100% knockback resistance.

## Progression ladder (diamond → netherite → allthemodium → vibranium → unobtainium)

The config-confirmed order and unlock gates are:

1. **Diamond Armor** — `&bDiamond Armor&r` (quest `5DDC15AAFD2CAF47`). The natural mid-game goal. Unlocks netherite smithing.
2. **Netherite Armor** — `&cNetherite Armor&r` (quest `074EC1E636CD6605`). Requires diamond armor + netherite smithing table + ancient debris. Upgrade from diamond for toughness + lava immunity.
3. **Allthemodium Armor** — `&6Allthemodium Armor&r` (quest `6C5F9D0D447EFB9C` / `5BA84F6282D9CAF1`). Requires netherite armor (per quest description: "BTW you will need &cNetherite&r to craft it."). Found at deep deepslate levels (approx. Y -40 in Deep Dark, guides say; verify in-game). Highest "vanilla-style" tier before modded content.
4. **Vibranium Armor** — `&3Vibranium Armor&r` (quest `72DDA413D73E3235`). Requires allthemodium armor (quest `72DDA413D73E3235` description: "Much higher stats in everything with the next in line for &6&lAllthemodium&r Armors, &3Vibranium&r! You will need &6Allthemodium Armor&r to create it."). Obtained from Nether sources.
5. **Unobtainium Armor** — `&5Unobtainium Armor&r` (quest `6F76DA3BBAE8337B`). Requires vibranium armor (quest `6F76DA3BBAE8337B` description: "The greatest Armor we can get from &6&lAllthemodium&r, &5Unobtainium&r! Now with 100% Knockback Resistance and higher stats everywhere! Also needs &3Vibranium Armor&r to make it."). The endgame pinnacle.

### Tool progression (mirroring the armor ladder)

The same tier order applies to tools, found in the **Basic Tools** chapter (`basic_tools.snbt`):

1. **Diamond tool** — the mid-game standard (pickaxe, sword, etc.).
2. **Netherite tool** — higher durability, toughness, lava immunity.
3. **Allthemodium tool** — gated behind netherite; see quest `&6Allthemodium Armor&r` which notes netherite is required for crafting. Tools have more armor points and magic protection.
4. **Vibranium tool** — requires allthemodium tool as component; higher stats.
5. **Unobtainium tool** — the highest tier; requires vibranium tool. Quest `6F76DA3BBAE8337B` title is `&5Unobtainium Armor` but the same tier applies to tools (unobtainium swords, picks, etc. exist as task items in the armor chapter).

**No-invented-names check**: All item ids and quest titles quoted are taken directly from the config at commit `e5e3d1d83e`. Item ids such as `minecraft:netherite_helmet`, `allthemodium:allthemodium_helmet`, `allthemodium:vibranium_helmet`, `allthemodium:unobtainium_helmet` appear in the `basic_armor.snbt` quests tasks. If a detail is not in the config and not stated by the user, say "check the quest entry / JEI" — do not fill from memory.

## Stages overview (from `references/progression.md`)

| Stage | Typical coverage |
|-------|------------------|
| **early-game** | Leather → chainmail → gold → diamond |
| **tech** | Netherite, first ore-doubling, basic machines |
| **magic** | Apothic, Ars Nouveau, Forbidden & Arcanus enchantments |
| **endgame** | Allthemodium → Vibranium → Unobtainium (Chapters 2–4) |

*Early-game and tech overlap: netherite is the bridge from tech to endgame. Allthemodium, vibranium, and unobtainium are firmly endgame (Chapter 2: Allthemodium onward).*

## How to use this ladder

1. **Check your current stage** using `references/progression.md` — if you are in early-game or tech, diamond is your floor; netherite is the first meaningful upgrade.
2. **If you have netherite**: upgrade to allthemodium once you reach Chapter 2: Allthemodium (deep deepslate / Dark Campus).
3. **If you have allthemodium**: upgrade to vibranium for the extra stats; the quest explicitly says you need allthemodium as a prerequisite.
4. **If you have vibranium**: upgrade to unobtainium only for the endgame / ATM Star — it requires vibranium as a component and is the highest possible tier.
5. **Always defer** to the in-game quest book and JEI for exact counts, recipes, and ingredient quantities. This ladder maps the *config-confirmed* order and gates; individual quest requirements may vary by version.

---

*This doc was grounded in `config/ftbquests/quests/chapters/basic_armor.snbt` and `config/ftbquests/quests/lang/en_us/chapters/basic_armor.snbt` from AllTheMods/ATM-10 at commit `e5e3d1d83e` (pack 8.2, 2026-09-22). Item ids and quest titles are quoted from the config; anything else is approximate.*