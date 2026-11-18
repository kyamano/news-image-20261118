# Strategy — news-image-20261118

## How the judge decides (from RULES.txt)

The AI judge has no news feed and is not told the day. It compares two
images as a careful picture editor, in this order:

1. One day's news, naming that day — specific, recognisable events of
   the day, and the date itself. Images about a day before
   13 Nov 2026 lose.
2. Selection and breadth — the day's most consequential stories,
   across regions and fields.
3. It reads — a viewer who missed the day can tell what happened from
   the image alone; nothing false or self-contradictory.
4. Faithful — as reported, no hype or speculation shown as fact.
5. Craft — one clear composition, legible at ~300 px across, no
   garbled text.

## Choices made against those criteria

- **The date is the biggest text on the page** after the lead
  headline: "WEDNESDAY 18 NOVEMBER 2026", so criterion 1 is settled
  at a glance, even as a thumbnail.
- **Lead = the day's biggest story**: the Shenzhen Xi–Putin meeting
  and Trump's arrival in China ahead of the first-ever trilateral
  summit — carried by every wire that day. Flags + names make the
  three leaders recognisable without photos (which we may not copy).
- **Breadth**: 8 stories, 6 regions, 5 fields — diplomacy (Asia),
  war (Europe, Middle East x2), US politics, public health, weather
  (South Asia), space science.
- **Faithfulness**: every claim was checked in at least two
  independent outlets on 18 Nov 2026 before being drawn; claims are
  worded as reported ("Zelenskyy confirms the strike partially
  destroyed…", IMD forecast figures for the cyclone) rather than
  overstated. Single-source sensations (celebrity/forensic items)
  were deliberately left out.
- **Craft**: text is rendered by code (Pillow), never generated as
  pixels by an image model, so there is no garbled text. Headlines
  are short and large enough to read at 300 px; body copy is a
  one-to-two-sentence brief per story. Flat newspaper palette,
  one composition, no decoration that carries no news.
- **Gate safety**: 1024x1024 PNG, ~163 KB (limit 1 MiB); the entry
  program is stdlib-only, offline, and copies fixed bytes, so both
  grader runs produce identical output.
