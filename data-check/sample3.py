import json, time, urllib.request, urllib.parse
UA="penombra-data-check/0.1 (personal research, no contact)"
def get(path):
    err=None
    for i in range(4):
        try:
            req=urllib.request.Request("https://musicbrainz.org/ws/2/"+path, headers={"User-Agent":UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                d=json.load(r); time.sleep(1.2); return d
        except Exception as e:
            err=str(e); time.sleep(3)
    print("FAIL",path[:70],err,flush=True); return None
plan=[("synthwave",o) for o in (0,100,200,300,400,500)]+[("darkwave",o) for o in (0,100,200,300,400,500,600)]+[("coldwave",o) for o in (0,100,200)]
out=[]
for tag,off in plan:
    q=urllib.parse.quote(f'tag:"{tag}"')
    d=get(f"artist?query={q}&fmt=json&limit=2&offset={off}")
    for a in (d or {}).get('artists',[]):
        rl=get(f"release?artist={a['id']}&status=official&limit=1&fmt=json")
        rs=(rl or {}).get('releases',[])
        if not rs:
            rl=get(f"release?artist={a['id']}&limit=1&fmt=json"); rs=(rl or {}).get('releases',[])
        if not rs: out.append(dict(tag=tag,artist=a['name'],none=True)); continue
        r=rs[0]
        x=get(f"release/{r['id']}?inc=artist-rels+recording-rels+labels+recordings+artist-credits&fmt=json")
        if not x: continue
        rels=list(x.get('relations',[])); tracks=0; trels=0
        for m in x.get('media',[]):
            for t in m.get('tracks',[]):
                tracks+=1; tr=t.get('recording',{}).get('relations',[]); trels+=len(tr); rels+=tr
        types={}
        for z in rels: types[z['type']]=types.get(z['type'],0)+1
        labs=[l['label']['name'] for l in x.get('label-info',[]) if l.get('label') and l['label']['name']!='[no label]']
        row=dict(tag=tag,artist=a['name'],title=x['title'],date=x.get('date',''),country=x.get('country',''),tracks=tracks,labels=labs,rels=types,has_credit=bool(rels))
        out.append(row); print(row,flush=True)
json.dump(out,open("sample3.json","w"),ensure_ascii=False)
n=[o for o in out if not o.get('none')]
print("\nSUMMARY releases",len(n),"with any credit rel",sum(o['has_credit'] for o in n),"with real label",sum(bool(o['labels']) for o in n),"with date",sum(bool(o['date']) for o in n),"with country",sum(bool(o['country']) for o in n))
for tag in ("synthwave","darkwave","coldwave"):
    s=[o for o in n if o['tag']==tag]
    print(tag,len(s),"credits",sum(o['has_credit'] for o in s),"labels",sum(bool(o['labels']) for o in s))
