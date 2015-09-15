
def read_weka_numeric_data(filename):
    file_  = open(filename, 'r')
    lines = file_.readlines()
    file_.close()
    
    _reading_data = False
    
    relation   = ""
    attributes = []
    data       = []
    
    for line in lines:
        if not _reading_data:
            if line.startswith("@relation"):
                relation = line[10:].strip()
            elif line.startswith("@attribute"):
                attribute = line[11:].split(" ")[0]
                attributes.append(attribute)
            elif line.startswith("@data"):
                _reading_data = True
        else:
            n_cols   = len(attributes)
            splitted = line.split(',')
            if len(splitted) == n_cols:
                data.append(map(float, splitted))
            else:
                error("some rows have different length")
    
    return { 'relation':   relation,
             'attributes': attributes,
             'data':       data
            }
