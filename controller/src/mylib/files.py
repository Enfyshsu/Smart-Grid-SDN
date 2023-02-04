import json

def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)