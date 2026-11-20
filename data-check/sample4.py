import json, time, urllib.request, urllib.parse, urllib.error
UA="penombra-data-check/0.1 (personal research, no contact)"
def get(url):
    err=None
    for i in range(4):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                d=json.load(r); time.sleep(1.2); return d
        except urllib.error.HTTPError as e:
            if e.code==404: time.sleep(1.2); return "404"
            err=str(e); time.sleep(3)
        except Exception as e:
            err=str(e); time.sleep(3)
    print("FAIL",url[:80],err,flush=True); return None
MB="https://musicbrainz.org/ws/2/"
plan=[("synthwave",o) for o in (0,100,200,300,400)]+[("darkwave",o) for o in (0,100,200,300,400)]+[("coldwave",o) for o in (0,100,200)]
out=[]
for tag,off in plan:
    q=urllib.parse.quote(f'tag:"{tag}"')
    d=get(MB+f"artist?query={q}&fmt=json&limit=2&offset={off}")
    for a in (d or {}).get('artists',[]) if isinstance(d,dict) else []:
        x=get(MB+f"artist/{a['id']}?inc=url-rels+artist-rels&fmt=json")
        if not isinstance(x,dict): continue
        urls={}
        for r in x.get('relations',[]):
            if 'url' in r:
                h=urllib.parse.urlparse(r['url']['resource']).netloc.replace('www.','')
                key=('bandcamp' if 'bandcamp' in h else 'discogs' if 'discogs' in h else 'spotify' if 'spotify' in h else 'youtube' if 'youtube' in h else 'soundcloud' if 'soundcloud' in h else 'other')
                urls[key]=urls.get(key,0)+1
        arel={}
        for r in x.get('relations',[]):
            if 'artist' in r: arel[r['type']]=arel.get(r['type'],0)+1
        rg=get(MB+f"release-group?artist={a['id']}&limit=3&fmt=json")
        art=[]
        for g in (rg or {}).get('release-groups',[]) if isinstance(rg,dict) else []:
            c=get(f"https://coverartarchive.org/release-group/{g['id']}")
            art.append(c!="404" and c is not None)
        row=dict(tag=tag,artist=a['name'],urls=urls,artist_rels=arel,cover=art)
        out.append(row); print(row,flush=True)
json.dump(out,open("sample4.json","w"),ensure_ascii=False)
n=len(out)
print("\nSUMMARY artists",n)
print("any url",sum(bool(o['urls']) for o in out),"bandcamp",sum('bandcamp' in o['urls'] for o in out),"discogs",sum('discogs' in o['urls'] for o in out),"spotify",sum('spotify' in o['urls'] for o in out))
print("artist-artist rels",sum(bool(o['artist_rels']) for o in out))
allc=[c for o in out for c in o['cover']]
print("release groups checked",len(allc),"with cover art",sum(allc))
for tag in ("synthwave","darkwave","coldwave"):
    s=[o for o in out if o['tag']==tag]; c=[x for o in s for x in o['cover']]
    print(tag,len(s),"bandcamp",sum('bandcamp' in o['urls'] for o in s),"artistrels",sum(bool(o['artist_rels']) for o in s),"cover",sum(c),"/",len(c))
