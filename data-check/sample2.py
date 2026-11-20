import json, time, urllib.request, urllib.parse
UA="penombra-data-check/0.1 (personal research, no contact)"
def get(path):
    for i in range(4):
        try:
            req=urllib.request.Request("https://musicbrainz.org/ws/2/"+path, headers={"User-Agent":UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                d=json.load(r); time.sleep(1.2); return d
        except Exception as e:
            err=str(e); time.sleep(3)
    print("FAIL",path,err); return None
def search(tag, off, n):
    q=urllib.parse.quote(f'tag:"{tag}"')
    d=get(f"artist?query={q}&fmt=json&limit={n}&offset={off}")
    return [(a['id'],a['name']) for a in (d or {}).get('artists',[])]
tail=[]
for tag,off in [("synthwave",600),("darkwave",400)]:
    for mbid,name in search(tag,off,6):
        rg=get(f"release-group?artist={mbid}&limit=1&fmt=json")
        rc=get(f"recording?artist={mbid}&limit=1&fmt=json")
        print(tag,off,name,(rg or {}).get('release-group-count'),(rc or {}).get('recording-count'),flush=True)
# credit density: first 3 releases of a mid artist (Karl Casey) with relationships
mb="synthwave"
arts=search("synthwave",0,6)
for mbid,name in arts[2:4]:
    rl=get(f"release?artist={mbid}&limit=3&fmt=json")
    for r in (rl or {}).get('releases',[]):
        d=get(f"release/{r['id']}?inc=artist-rels+recording-rels+labels+recordings+artist-credits&fmt=json")
        if not d: continue
        rels=list(d.get('relations',[]))
        for m in d.get('media',[]):
            for t in m.get('tracks',[]): rels+=t.get('recording',{}).get('relations',[])
        types={}
        for x in rels: types[x['type']]=types.get(x['type'],0)+1
        print("CREDITS",name,'|',d['title'],'| tracks',sum(len(m.get('tracks',[])) for m in d.get('media',[])),'| labels',[l['label']['name'] for l in d.get('label-info',[]) if l.get('label')],'| rels',types,flush=True)
