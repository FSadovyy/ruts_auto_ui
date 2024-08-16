import os
import json
from .path import custom_path

__DATA_DIRECTORY = custom_path("/data")
valid_datatypes = [x.split("_data.")[0] for x in filter(lambda x: "_data.json" in x, os.listdir(__DATA_DIRECTORY))]


def data(*datatype: str or tuple) -> dict:
    ourdatas = []
    if type(datatype) is str:
        datatype = (datatype,)
    print(valid_datatypes)
    for x in datatype:
        if x not in valid_datatypes:
            raise ValueError("Invalid data type in json link")
        json_link = __DATA_DIRECTORY + f"/{x}_data.json"
        ourdatas.append(json.load(open(json_link, encoding='utf8')))
    return ourdatas[0] if len(ourdatas) == 1 else ourdatas
