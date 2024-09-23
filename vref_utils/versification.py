import os

# distributed with ./vref.txt - the "org" (standard) versification vref file
org_vref_dot_txt_path = os.path.join(os.path.dirname(__file__), "vref.txt")


def get_versification_mapping(versification_vref_path=org_vref_dot_txt_path):
    """
    Returns a mapping of verse references to line numbers based on a vref
    file that has a reference on each line corresponding to verse-per-line
    vref files that use the same versification system.
    """
    with open(versification_vref_path) as f:
        vref = f.readlines()
        vref = {line.strip(): index + 1 for index, line in enumerate(vref)}
    return vref


def get_versification_range(start, end, versification_mapping):
    """
    Returns a list of verse references between the start and end verse
    references
    """
    reverse_mapping = {value: key for key, value in versification_mapping.items()}
    start_line = versification_mapping[start]
    end_line = versification_mapping[end]
    return [reverse_mapping[line] for line in range(start_line, end_line + 1)]
