import json, time, urllib.request, urllib.parse
UA="penombra-data-check/0.1 (personal research, no contact)"
def get(path, tries=4):
    for i in range(tries):
        try:
            req=urllib.request.Request("https://musicbrainz.org/ws/2/"+path, headers={"User-Agent":UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                d=json.load(r); time.sleep(1.2); return d
        except Exception as e:
            time.sleep(3)
    return None
def search(tag, off, n):
    q=urllib.parse.quote(f'tag:"{tag}"')
    d=get(f"artist?query={q}&fmt=json&limit={n}&offset={off}")
    return [(a['id'],a['name']) for a in (d or {}).get('artists',[])]
rows=[]
for label,tag,off in [("top synthwave","synthwave",0),("tail synthwave","synthwave",900),("top darkwave","darkwave",0),("tail darkwave","darkwave",550)]:
    for mbid,name in search(tag,off,6):
        rg=get(f"release-group?artist={mbid}&limit=1&fmt=json")
        rc=get(f"recording?artist={mbid}&limit=1&fmt=json")
        rows.append((label,name,(rg or {}).get('release-group-count'),(rc or {}).get('recording-count')))
        print(rows[-1], flush=True)
json.dump(rows,open("sample.json","w"))
