import json, os

def load_schema(name, folder=os.path.join("data", "schemas")):
    with open(os.path.join(folder, name), "r", encoding="utf-8") as file:
        schema = json.load(file)
    return schema