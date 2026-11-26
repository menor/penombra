# Penombra

A visual catalogue of synthwave and darkwave built on MusicBrainz data, with lists kept by guests and members.

## Catalogue

**Catalogue**:
Penombra's copy of the MusicBrainz artists and release groups that carry at least one core tag.
_Avoid_: dataset, database, library

**Artist**:
A person or group credited on a release group, as MusicBrainz records it.
_Avoid_: band, act

**Release group**:
One musical work across all its editions, such as an album, EP or single. Each tile in the grid and each row in the table is one release group.
_Avoid_: record, album (an album is one type of release group)

**Release**:
One edition of a release group, with its own country, label, date and cover.
_Avoid_: pressing, version

**Cover**:
The front image of a release, shown for its release group. Some release groups have none.
_Avoid_: artwork, album art, thumbnail

**Label**:
The company that published a release. A release group can have several labels through its releases.
_Avoid_: publisher, imprint

**Tag**:
A word that MusicBrainz users vote onto an artist or a release group. One item can carry many tags.
_Avoid_: genre, sub-genre, style

**Core tag**:
One of the 6 tags that admit an item into the catalogue: synthwave, darkwave, coldwave, retrowave, outrun, dark synth. A release group with 2 core tags belongs to both.
_Avoid_: genre, sub-genre, category

**Synthetic rows**:
Generated data for stress tests. Never part of the catalogue, and always labelled as synthetic.
_Avoid_: fake data, test catalogue

## People and lists

**Guest**:
A person using Penombra without credentials. A guest can keep private lists for 30 days.
_Avoid_: user, visitor, anonymous user

**Member**:
A person who has signed up. Signing up turns a guest into a member and keeps the guest's lists.
_Avoid_: user, account, person (MusicBrainz uses Person as an artist type)

**List**:
A named, ordered set of entries with one owner. It is private or public.
_Avoid_: collection, playlist, crate

**Entry**:
One release group in one list, with its position and an optional entry link. A release group appears at most once per list.
_Avoid_: item, list item

## Links

**Buy link**:
A Bandcamp album URL attached to a release group or one of its releases, on the artist's or the label's Bandcamp.
_Avoid_: store link, purchase link

**Search link**:
A generated Bandcamp search for an artist and a title. Shown when no buy link exists, and labelled as a search.
_Avoid_: buy link, fallback link

**Artist link**:
The home page of an artist on Bandcamp, Discogs or Spotify. Never a buy link.

**Label link**:
The home page of a label on Bandcamp. Never a buy link.

**Entry link**:
A URL that a guest or member attaches to an entry.
_Avoid_: custom link, user link
