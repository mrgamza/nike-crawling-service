import json


def make_json(dictionary):
    return json.dumps(dictionary, default=str)
