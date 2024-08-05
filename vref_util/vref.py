import linecache
import os

# distributed with ./vref.txt
vref_dot_txt_path = os.path.join(os.path.dirname(__file__), "vref.txt")

with open(vref_dot_txt_path) as f:
    vref = f.readlines()
    vref = {
        line.strip(): index
        for index, line in enumerate(vref)
    }

class Vref:
    def __init__(self, vref_file):
        self.vref_file = vref_file
    def __getitem__(self, key: str):
        line = vref[key]
        return linecache.getline(self.vref_file, line + 1).strip()