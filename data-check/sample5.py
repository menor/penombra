import json, time, urllib.request, urllib.parse, urllib.error
UA="penombra-data-check/0.1 (personal research, no contact)"
def get(url):
    err=None
    for i in range(4):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                d=json.load(r); time.sleep(1.1); return d
        except urllib.error.HTTPError as e:
            if e.code==404: time.sleep(1.1); return "404"
            err=str(e); time.sleep(3)
        except Exception as e:
            err=str(e); time.sleep(3)
    print("FAIL",url[:90],err,flush=True); return None
MB="https://musicbrainz.org/ws/2/"
def kind(h):
    for k in ("bandcamp","discogs","spotify","youtube","soundcloud"):
        if k in h: return k
    return "other"
out=[]; seen=set()
for tag in ("synthwave","darkwave","coldwave"):
    for L in ("b","f","k","n","r","v"):
        q=urllib.parse.quote(f'tag:"{tag}" AND artist:{L}*')
        d=get(MB+f"artist?query={q}&fmt=json&limit=4&offset=0")
        if not isinstance(d,dict): continue
        for a in d.get('artists',[]):
            if a['id'] in seen: continue
            seen.add(a['id'])
            x=get(MB+f"artist/{a['id']}?inc=url-rels&fmt=json")
            if not isinstance(x,dict): continue
            urls=set()
            for r in x.get('relations',[]):
                if 'url' in r: urls.add(kind(urllib.parse.urlparse(r['url']['resource']).netloc))
            rg=get(MB+f"release-group?artist={a['id']}&limit=2&fmt=json")
            if not isinstance(rg,dict): continue
            nrg=rg.get('release-group-count',0)
            cover=[]
            for g in rg.get('release-groups',[]):
                c=get(f"https://coverartarchive.org/release-group/{g['id']}")
                cover.append(c!="404" and c is not None)
            rl=get(MB+f"release?artist={a['id']}&limit=1&fmt=json")
            rbc=None
            if isinstance(rl,dict) and rl.get('releases'):
                rx=get(MB+f"release/{rl['releases'][0]['id']}?inc=url-rels&fmt=json")
                if isinstance(rx,dict):
                    ru={kind(urllib.parse.urlparse(r['url']['resource']).netloc) for r in rx.get('relations',[]) if 'url' in r}
                    rbc='bandcamp' in ru
            row=dict(tag=tag,letter=L,artist=a['name'],rgs=nrg,urls=sorted(urls),cover=cover,release_bandcamp=rbc)
            out.append(row); print(row,flush=True)
json.dump(out,open("sample5.json","w"),ensure_ascii=False)
def summ(rows,label):
    if not rows: print(label,"none"); return
    c=[x for o in rows for x in o['cover']]
    rb=[o['release_bandcamp'] for o in rows if o['release_bandcamp'] is not None]
    print(f"{label}: artists {len(rows)} | any link {sum(bool(o['urls']) for o in rows)} | artist bandcamp {sum('bandcamp' in o['urls'] for o in rows)} | discogs {sum('discogs' in o['urls'] for o in rows)} | spotify {sum('spotify' in o['urls'] for o in rows)} | release-level bandcamp {sum(rb)}/{len(rb)} | cover {sum(c)}/{len(c)}")
print("\nSUMMARY")
summ(out,"all")
summ([o for o in out if o['rgs']<=5],"tail (<=5 release groups)")
summ([o for o in out if o['rgs']<=2],"deep tail (<=2)")
for t in ("synthwave","darkwave","coldwave"): summ([o for o in out if o['tag']==t and o['rgs']<=5],"tail "+t)
