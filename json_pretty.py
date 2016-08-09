#!/usr/bin/python3
import json

filename = "diagostore.json"

json_data = open(filename).read()
data = json.loads(json_data)
pretty_json = json.dumps(data, indent=4, sort_keys=True)
with open('pretty_json.json', 'w') as outfile:
    outfile.write(pretty_json)
    outfile.close()