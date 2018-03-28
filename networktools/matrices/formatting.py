def add_padding(parts): 
    max_size = max([len(part) for part in parts])

    return [tuple(part) + ('',)*(max_size - len(part)) for part in parts]