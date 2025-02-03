def list_elem_length(items_list):
    length = 0
    for item in items_list:
        if isinstance(item, int):
            length += len(str(item)) + 2 # need to add 2 for the control characters
        elif isinstance(item, list):
            length += list_elem_length(item) + 2
        else:
            length += len(item) + 2
    return length

def dict_elem_length(items_dict):
    length = 0
    for key, value in items_dict.items():
        length += len(key) + 2
        if isinstance(value, int):
            length += len(str(value)) + 2
        elif isinstance(value, list):
            length += list_elem_length(value) + 2
        elif isinstance(value, dict):
            length += dict_elem_length(value) + 2
        else:
            length += len(value) + 2
    return length
