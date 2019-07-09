# remove_duplicates.py

SEEN = {}
def remove_duplicates(rows, key):
    global SEEN
    
    if key not in SEEN.keys():
        SEEN[key] = set()
        
    for r in rows:
        if r[key] not in SEEN[key]:
            SEEN[key].add(r[key])
            yield r
