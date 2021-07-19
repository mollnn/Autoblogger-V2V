import json

def readConfig(key, filename="../config/main.json"):
    f=open(filename, "r")
    obj=json.load(f)
    f.close()
    return obj[key]