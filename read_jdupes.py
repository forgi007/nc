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

def read_jdupes(jdupes_filename):
    lst=load_jdupes_json(jdupes_filename)
    jdupe_set=set()
    for dup in lst:
        dupes=[]
        for file in dup["fileList"]:
            dupes.append(file["filePath"])
        jdupe_set.add(tuple(dupes))
    return jdupe_set