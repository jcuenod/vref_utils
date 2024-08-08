import os

# distributed with ./vref.txt - the "org" (standard) versification vref file
org_vref_dot_txt_path = os.path.join(os.path.dirname(__file__), "vref.txt")

def get_versification_mapping(vrs_path=org_vref_dot_txt_path):
    with open(vrs_path) as f:
        vref = f.readlines()
        vref = {
            line.strip(): index + 1
            for index, line in enumerate(vref)
        }
    return vref

def get_versification_range(start, end, versification_mapping):
    reverse_mapping = {
        value: key
        for key, value in versification_mapping.items()
    }
    start_line = versification_mapping[start]
    end_line = versification_mapping[end]
    return [reverse_mapping[line] for line in range(start_line, end_line + 1)]