# Ballistics and Damage

G.A.M.M.A. inherits Anomaly's ballistic model: every bullet carries hit
power and a penetration value, and every piece of armor has protection
per body region. Fights are decided as much by ammo choice as by aim.

## Damage basics

- Each ammo type defines how hard it hits and how well it penetrates.
  Armor then mitigates the hit based on the protection of the body part
  struck — headshots against helmets behave differently from torso hits.
- If a bullet's penetration beats the armor's protection, most of the
  damage goes through. If it does not, the armor absorbs a large share
  and the target may shrug the hit off.
- Heavier calibers generally hit harder; smaller, faster rounds depend
  more on placement and ammo type.

## Ammo types

- **Ball / FMJ**: balanced standard rounds, decent against soft targets,
  mediocre against armor.
- **Armor-piercing (AP)**: built to defeat protective gear. Noticeably
  better against armored stalkers and exoskeletons, but accelerates
  barrel wear — maintain the weapon more often.
- **Expansive / hollow-point**: dump energy into soft tissue for heavy
  damage to unarmored targets, but perform poorly against armor.
- Concrete example: 9x39mm **SP-5** is the accurate, flat-shooting round
  that holds velocity at range, while **SP-6** sacrifices some of that
  for superior penetration. Choose per expected opposition.

## Armor and penetration

- Protection runs from light jackets and trenchcoats up through stalker
  suits, heavy combat armor, and exoskeletons — each step meaningfully
  harder to punch through.
- Firing low-penetration ammo at heavy armor wastes bullets: hits may
  deflect or deal only a fraction of their damage.
- Conversely, AP ammo against unarmored targets can over-penetrate,
  wasting some of its potential — match ammo to target.
- Popular community overhauls (such as the well-known ballistics addon)
  formalize this into armor classes with deflection, partial, full, and
  overkill penetration bands; the base game follows the same logic more
  loosely.

## Range and accuracy

- Damage falls off with distance, and rounds lose velocity — the farther
  the shot, the weaker and less accurate it gets.
- Subsonic and heavy rounds drop faster; flatter-shooting rounds like
  SP-5 stay effective further out than SP-6.
- Zero your expectations: a round that one-taps at 50 meters may only
  wound at 200.

## Wounds and bleeding

- Gunshots and mutant hits cause bleeding, which drains health over time
  until treated.
- Bandages stop bleeding; medkits restore health. Carry both — bleeding
  out after winning a fight is an embarrassing way to die.
- Heavy bleeding may need stronger medical items; light scratches can be
  bandaged between engagements.

## Mutants

- Mutants do not wear armor, so expansive rounds and raw hit power shine
  against them.
- Different mutants have different toughness — small, fast ones die to a
  few well-placed shots, while large ones demand sustained fire or AP
  rounds to reach vitals.
- Aim for the head where possible; body shots on thick-hided mutants
  waste ammunition.

## Tips

- Scout your enemy: bandits in jackets die to anything, Monolith in
  exoskeletons demand AP.
- Keep two magazines' worth of AP and standard ammo and swap per target.
- Maintain the barrel — a worn gun firing AP ammo wears out fast.
