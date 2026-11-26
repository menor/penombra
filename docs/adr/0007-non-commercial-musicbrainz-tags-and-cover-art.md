---
status: accepted
date: 2026-11-25
---

# Non-commercial use of MusicBrainz tags and cover art

Penombra stays non-commercial: no ads and no paid tier. MusicBrainz core data (artists, release groups, releases, labels, relationships and URLs) is CC0, but tags, including genre associations, are CC BY-NC-SA 3.0, and the catalogue is defined by core tags. So the site credits MusicBrainz, labels tag data CC BY-NC-SA 3.0 wherever it is shown or exported, including MCP answers, and earns no money. Checked on 25 November 2026 against the MusicBrainz data licence and database pages. This is a reading of the documentation, not legal advice.

## Considered options

- **Use only CC0 data.** Rejected: without tags there is no catalogue, and genre associations carry the same licence as tags.
- **A commercial licence from the MetaBrainz Foundation.** Not needed while the site earns nothing.

## Cover art

Cover images are "copyrighted by their respective copyright owners", and no licence is granted. Nothing forbids a third-party site from showing them. MusicBrainz itself deep links them from Internet Archive servers. The Internet Archive terms limit use to non-commercial, non-infringing or fair use, so they also depend on Penombra staying non-commercial. Checked on 26 November 2026: [research note](https://github.com/menor/penombra/blob/research/cover-art-archive/research/cover-art-archive.md). This is not legal advice.

- **Source.** The browser loads each cover from coverartarchive.org. There is no proxy, and the site stores no copies. A `preconnect` to coverartarchive.org and archive.org cuts the redirect cost. Phase 3 measures it against S5. Cost: each visitor's IP address reaches archive.org.
- **Which image.** The import records, for each release group, whether it has a cover and which release holds it. The browser requests `/release/{mbid}/front-250`, which is 1 redirect. If the dumps lack the cover art tables, use `/release-group/{mbid}/front-250` instead. Phase 2 checks this.
- **Sizes.** Tiles use 250 px, with 500 px in `srcset` for 2x screens. Artist and release group pages use 500 px. 1200 px is not used.
- **Fallback.** One tile, drawn in CSS, shows the title and artist. It covers a missing cover at import and any failed image load (404, takedown, 503).
- **Alt text.** "Cover of {title} by {artist}".
- **Credit.** The footer links to musicbrainz.org and coverartarchive.org.
- **Removal.** Rights holders ask the Internet Archive to remove an image. GitHub issues are the second route.

Bandcamp and Discogs images were rejected. Their terms restrict reuse more than the Cover Art Archive does.

## Consequences

- The app code stays MIT. The licence binds the data, not the code.
- Any export of tag data is CC BY-NC-SA 3.0, never CC0.
- Revisit before any plan to earn money from the site.
