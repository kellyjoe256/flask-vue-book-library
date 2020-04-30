import json


def convert_to_dict(data):
    return json.loads(data.decode('utf-8'))
