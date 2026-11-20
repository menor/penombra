# Data check: what MusicBrainz holds for synthwave and darkwave

Run on 11 November 2026 against the public MusicBrainz API and the Cover Art Archive.
Purpose: decide scope before building. The result killed the credits explorer.

## How to run

```
python3 -I sample3.py
```

- Python 3 standard library only. No installs.
- Each script waits 1.1 to 1.2 seconds between calls. MusicBrainz allows about 1 request per second.
- The User-Agent is `penombra-data-check/0.1 (personal research, no contact)`. MusicBrainz asks for a contact in the User-Agent. Add a project contact before running at volume.
- Results change as MusicBrainz data changes. Rerun to refresh.

## Scripts

| Script | What it did | Saved output |
|---|---|---|
| `sample.py` | Release-group and recording counts for 12 top-ranked artists | `sample.json` (only the 12 completed rows) |
| `sample2.py` | 6 darkwave artists from search offset 400. Credit relationships for 6 releases by 2 synthwave artists | Printed only. Results below |
| `sample3.py` | One release per artist for 26 artists. Date, country, label, credit relationships | `sample3.json` |
| `sample4.py` | Links, artist-to-artist relationships and cover art for 26 artists | `sample4.json` |
| `sample5.py` | 69 artists chosen by name initial. Links, release-level Bandcamp, cover art | `sample5.json` |

## Tag counts (search API, 11 November 2026)

These came from one-off curl commands. They were not saved to a file.

| Tag | Artists | Release groups |
|---|---|---|
| synthwave | 1,222 | 14,361 |
| darkwave | 728 | 481 |
| coldwave | 345 | 2,788 |
| retrowave | 121 | 276 |
| outrun | 20 | 91 |
| dark synth | 18 | 13 |
| minimal wave | 168 | 590 |
| italo disco | 219 | 3,643 |
| EBM | 709 | 16,031 |
| synth-pop | 1,960 | 50,742 |

Counts include every tagged item whatever its vote count. Vote thresholds were not measured.
Core tags (synthwave, darkwave, coldwave, retrowave, outrun, dark synth) total at most about 2,450 artists and 18,000 release groups. Overlap between tags is unknown.
The wider tags (minimal wave, italo disco, EBM, synth-pop) are recorded for reference only. The catalogue stays on the core tags.

## Results

### Size per artist (`sample.py`, 12 artists)
- Well-known: 22 to 259 release groups, 394 to 2,894 recordings.
- Long tail (6 darkwave artists from offset 400, `sample2.py`): 2 to 24 release groups, 12 to 177 recordings.

Rough estimate: under 1M rows for the core subset. This is an order of magnitude from 18 artists, not a measurement.

### Metadata and credits (`sample3.py`, 26 releases)

| Field | Present |
|---|---|
| Date | 26 of 26 |
| Country | 24 of 26. Many are "XW" (worldwide, digital) |
| Real label | 13 of 26. Synthwave 2 of 10, darkwave 5 of 10, coldwave 6 of 6 |
| Any credit relationship | 5 of 26 |
| Person credit (producer, mixer, engineer) | 1 of 26 |

The 5 credits were mostly artwork, illustration, a lacquer cut, and programming and recording on John Carpenter's *Halloween*.
`sample2.py` found zero credit relationships in 6 releases by Michael Oakley and Karl Casey.

### Links, relationships, covers (`sample4.py`, 26 artists)

| Field | Result |
|---|---|
| Any external link | 26 of 26 |
| Bandcamp | 21 (81%) |
| Discogs | 22 |
| Spotify | 19 |
| Artist-to-artist relationships | 11 of 26. Mostly "member of band" |
| Cover art | 67 of 73 release groups (92%) |

### Larger sample (`sample5.py`, 69 artists, 23 per tag)

| Group | Artists | Artist Bandcamp | Release Bandcamp | Cover art |
|---|---|---|---|---|
| All | 69 | 54 (78%) | 24 of 69 (35%) | 127 of 136 (93%) |
| More than 15 release groups | 46 | 37 | 17 of 46 | 89 of 92 |
| 6 to 15 release groups | 16 | 14 | 6 of 16 | 27 of 32 |
| 5 or fewer (true tail) | 7 | 3 | 1 of 7 | 11 of 12 |

Discogs 60 of 69 (87%). Spotify 56 of 69 (81%). Every artist had at least one external link.

## Limits

1. **The search API rejects offsets of 500 and above** with HTTP 400. Sampling stopped at rank 400 per tag.
2. **The true tail is unmeasured.** Only 7 of 69 artists had 5 or fewer release groups. The median was 20. Search ranks by score, so well-documented artists dominate.
3. **One release per artist** in `sample3.py`, chosen by API default order. Not random.
4. **Cover art was tested for existence.** Image size and load speed were not tested.
5. **Bandcamp links come from MusicBrainz URL relationships.** Missing in MusicBrainz does not mean missing on Bandcamp.
6. **Data licence and Cover Art Archive terms are unverified for a public site.** Check before launch.

## What the next step needs

The data dumps give exact counts for everything above, including the tail. Build the import script in Phase 2 of `../plan.md`, then replace these estimates with real numbers.
