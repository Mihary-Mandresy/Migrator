import os.path as path
import json
import argparse
from datetime import datetime
from math import inf

def getConfig():
    base_dir = path.dirname(path.dirname(path.abspath(__file__)))
    conf_path = path.join(base_dir, "conf", "conf.json")
    
    with open(conf_path, "r") as f:
        return json.load(f)
    
def getArgumentParser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-m", action="store_true")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-d", action="store_true")
    
    parser.add_argument('--pos', type=int, default=0)
    parser.add_argument('--limite', type=int, default=inf)
    
    return parser.parse_args()

def migratorInfoDir(dirname : str):
    [pos, date] = dirname.split("_")
    return {
        "pos": int(pos),
        "date": datetime.fromisoformat(date)
    }
