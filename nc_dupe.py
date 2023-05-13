import json
from pathlib import Path

def load_jdupes_json(jdupes_json):
    with open(jdupes_json) as json_data:
        try:
            json_str = json.load(json_data)
        except Exception as e:
            return False

        m=json_str["matchSets"]
        if m:
            print("commandLine="+json_str["commandLine"])
            print(f"Number of matches={len(m)}")
            return m
        else:
            return None

def dp_partial_find(what, lst):
    for l in lst:
        for w in what:
            if w in l:
                return l
    return None

#lst=load_jdupes_json("test.json")
lst=load_jdupes_json("dup.json")
dup_path=[]
for i,dup in enumerate(lst):
    file_list=[]
    #print(f"Duplicate {i}:")
    plst=[]
    for file in dup["fileList"]:
        f=Path(file["filePath"])
        n=f.name
        p=f.parent.resolve()
        #file_list.append(f)
        #print(f"p:{p} n:{n}")
        plst.append(p)
    lst=dp_partial_find(plst, dup_path)
    if not lst:
        dup_path.append(plst)

for i, d in enumerate(dup_path):
    print(f"{i}:\n" + '\n'.join([str(l) for l in d]))