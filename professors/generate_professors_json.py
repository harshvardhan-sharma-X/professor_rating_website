input_file = "professor_names.txt"
output_file = "data.json"

data =[]

with open(input_file, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f, start=1):
        name = line.strip()
        if name:
            data.append({
                "model" : "professors.professor",
                "pk" : idx,
                "fields" : {"name" : name}
            })

import json
with open(output_file, 'w', encoding="utf-8") as f:
    json.dump(data, f, indent=2) 