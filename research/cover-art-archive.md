# May a third-party site show Cover Art Archive images?

Research for issue #35. Checked 26 November 2026. This is a reading of public documents, not legal advice.

## Answer

Yes, in practice. No document grants a licence, and none forbids display.

- The Cover Art Archive grants no licence. The copyright stays with the owners. Use is "at your own risk". [1] [2] [3]
- Its API exists for third parties. It has no rate limit and serves 250, 500 and 1200 px thumbnails. [4]
- MusicBrainz itself shows the images by deep linking to Internet Archive servers. [5]
- A MusicBrainz reply on 20 November 2026 says there are no licensing requirements. It asks for a link back to MusicBrainz. [6]
- Takedown goes through the Internet Archive, which removes single images on complaint. [5] [6]
- The Internet Archive terms limit use to non-commercial, non-infringing or fair use. Penombra is non-commercial (ADR 0007). [7]

Bandcamp and Discogs are weaker alternatives. Both restrict reuse more than the Cover Art Archive does.

## Verified facts

Each fact quotes or paraphrases the cited page, read on 26 November 2026.

### Licence and copyright

1. The Cover Art Archive home page says: "All images are copyrighted by their respective copyright owners." It links no terms page. [1]
2. The MusicBrainz Cover Art Archive page says the covers "are being collected for archival purposes, and the collection will be accessible to the public. Use the images at your own risk." It asks users to "Be respectful of the rights of the artists and labels." [2]
3. The MusicBrainz data licence page says: "The MusicBrainz dataset does not contain cover art. Cover art is provided by the Cover Art Archive." So the CC0 and CC BY-NC-SA licences do not cover the images. [8]
4. The 2012 launch post says: "since we are not lawyers, we can not say what can and can not be done with these. So use them at your own risk!" [3]

### Hotlinking, sizes and rate limits

5. The API page says: "Any requests to fetch cover art must go through the coverartarchive.org service." [4]
6. Image endpoints return a 307 redirect to the binary image. A test request for one `front-250` image returned 307 to an `archive.org/download/...` URL, with `access-control-allow-origin: *`. [4]
7. "The current supported thumbnail sizes are 250px, 500px, and 1200px." The keys `small` and `large` are deprecated aliases for 250 and 500. A thumbnail request "may resolve to a 404 if the thumbnail does not exist." [4]
8. "There are currently no rate limiting rules in place at http://coverartarchive.org." The response list still names a 503 for an exceeded rate limit. [4]
9. A MusicBrainz banner on 26 November 2026 warns that thumbnail generation has a backlog at the Internet Archive. [2]
10. The API page says nothing about hotlinking, caching or attribution. [4]

### How MusicBrainz itself shows the images

11. The MusicBrainz copyright page says no images reside on MusicBrainz servers. "MusicBrainz displays images that are loaded from Internet Archive servers (via deep linking) directly." [5]

### Attribution, rate rules and takedown, from the forum

12. On 20 November 2026 a MusicBrainz team reply to a free, non-commercial app developer said: "There are no licensing requirements for the Cover Art Archive." It is "provided as-is and we don't offer a license as such, since we do not own the rights to the artwork." [6]
13. The same reply asked for "no specific wording, just point people back to us", and suggested mentioning donations. [6]
14. It asked the developer to follow "our rate limiting and user agent rules". That points at the MusicBrainz API rules: about 1 request per second and a real User-Agent. [6] [9]
15. It said: "specific pieces of artwork are taken down by the Internet Archive if someone complains about them." It also advised consulting legal counsel. [6]
16. The MusicBrainz copyright page tells rights holders to ask the Internet Archive by email to remove an image. [5]
17. In a 2024 thread, a MusicBrainz team member said hosting covers on MetaBrainz servers was "one step too dangerous" for the board. [10]

### Internet Archive terms

18. The Internet Archive terms page needs JavaScript. The tools used here could not render it. Its wording is quoted on an Internet Archive forum thread: "Access to the Archive's Collections is provided at no cost to you and is granted for scholarship and research purposes only. In particular, you certify that your use of any part of the Archive's Collections will be noncommercial and will be limited to noninfringing or fair use under copyright law." [7] [11]
19. The Internet Archive access policy, updated 29 August 2023, commits to "free and open access to its collections" for education, research and public interest. It points to the terms of use. [12]

### Alternatives

20. **Bandcamp.** Terms effective 7 May 2026. "Use, reproduction, modification, distribution or storage of any Content for other than personal, non-commercial use" is "expressly prohibited without prior written permission from Company, or from the copyright holder." The terms do not mention embeds. [13]
21. Bandcamp offers an official embedded player. Artists and fans make it from the Share/Embed control on an album page. [14]
22. **Discogs.** The API terms page sits behind a bot check and could not be read. Secondary sources quote it: images are "Restricted Data", image URLs need authentication, content may not be shown if more than 6 hours older than Discogs, and "Data provided by Discogs" must sit next to the data. [15] [16]

## Inference

These points follow from the facts. No source states them.

- Penombra's current plan fits the documented practice. ADR 0007 loads images from coverartarchive.org, stores no copies and credits the archive. MusicBrainz does the same (fact 11).
- "Non-commercial" carries weight twice: in the tag licence (ADR 0007) and in the Internet Archive terms (fact 18). A paid tier or ads would reopen both.
- Hotlinking keeps takedown simple. When the Internet Archive removes an image, Penombra's tile falls back on its own. A stored copy would need a separate removal step.
- The "personal, non-commercial" clause on Bandcamp makes copying its artwork riskier than the Cover Art Archive. The embedded player is the sanctioned route, but it plays audio. Audio playback is out of scope in `plan.md`.
- Discogs adds a login token, a 6-hour freshness rule and per-item attribution. It is not worth it for the 7% of covers that are missing.
- The 1200 px size is the largest thumbnail. Grid tiles need 250 px. Artist and release pages need 500 px.

## Not verified

- The live text and date of the Internet Archive terms page (fact 18 is a quote by others).
- The live text of the Discogs API terms (fact 22 is from secondary sources).
- The forum reply in fact 12 comes from a MusicBrainz team account. It is a forum answer, not a policy page.
- Whether the Internet Archive treats a hotlinking site as "use of the Collections" under its terms.
- Whether any rights holder has ever sent a takedown to a third-party site that hotlinks the archive. Fact 15 says MusicBrainz knows of no issues.

## Consequences for Penombra

- Keep loading images from coverartarchive.org. Store no copies.
- Request `front-250` for tiles and `front-500` for pages. Keep the fallback tile for 404s, including missing thumbnails (facts 7 and 9).
- Keep the footer credit. Link it to musicbrainz.org and coverartarchive.org (fact 13).
- Send image requests from the browser only. Any server-side calls follow the MusicBrainz rate and User-Agent rules (fact 14).
- Point removal requests to the Internet Archive as well as to GitHub issues (facts 15 and 16).
- ADR 0007 can replace "Whether a third-party site may show the images is not verified" with a link to this note.

## Sources

All read on 26 November 2026.

1. Cover Art Archive home page: https://coverartarchive.org/
2. MusicBrainz, Cover Art Archive: https://musicbrainz.org/doc/Cover_Art_Archive
3. MetaBrainz blog, "Announcing the Cover Art Archive", 9 October 2012: https://blog.metabrainz.org/2012/10/09/announcing-the-cover-art-archive/
4. MusicBrainz, Cover Art Archive API: https://musicbrainz.org/doc/Cover_Art_Archive/API
5. MusicBrainz, Copyright and DMCA Compliance: https://musicbrainz.org/doc/Copyright_and_DMCA_Compliance
6. MetaBrainz Community forum, "artwork copyright question", reply of 20 November 2026: https://community.metabrainz.org/t/artwork-copyright-question/816080
7. Internet Archive, Terms of Use: https://archive.org/about/terms.php
8. MusicBrainz, Data License: https://musicbrainz.org/doc/About/Data_License
9. MusicBrainz API rate limiting: https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting
10. MetaBrainz Community forum, "Implementing an alternative to the coverartarchive", 29 October 2024: https://community.metabrainz.org/t/implementing-an-alternative-to-the-coverartarchive/720408
11. Internet Archive forum, "Terms of Use - Scholarship and Research Purposes Only": https://archive.org/post/1101677/terms-of-use-scholarship-and-research-purposes-only
12. Internet Archive Access Policy, updated 29 August 2023: https://help.archive.org/help/internet-archive-access-policy/
13. Bandcamp Terms of Use, effective 7 May 2026: https://bandcamp.com/terms_of_use
14. Bandcamp help, "How do I create a Bandcamp embedded player?": https://get.bandcamp.help/en/articles/15263071-how-do-i-create-a-bandcamp-embedded-player
15. Discogs API Terms of Use (not readable by the tools used): https://support.discogs.com/hc/en-us/articles/360009334593-API-Terms-of-Use
16. Secondary quote of the Discogs 6-hour and attribution clauses: https://github.com/asuteau/sillon/issues/43
