import glob
import json
import os
from typing import List

from timed_rotating_text_file import TimedRotatingTextFile


def write(data: json) -> None:
    storage_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data.json")
    with TimedRotatingTextFile(storage_file, when="m", backup_count=5) as fp:
        fp.write(data + "\n")


def read() -> List[str]:
    file_manes = [f for f in glob.glob("../*.json*")]
    file_manes.reverse()
    data = ""
    for file_name in file_manes:
        with open(file_name) as fp:
            data += fp.read()
    data_list = data.split("\n")
    data_list.remove("")
    return data_list
