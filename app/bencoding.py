from app.utils import dict_elem_length, list_elem_length

def encode_bencode(py_obj):
    if isinstance(py_obj, int):
        return str(f"i{py_obj}e").encode()
    if isinstance(py_obj, str):
        return str(f"{len(py_obj)}:{py_obj}").encode()
    if isinstance(py_obj, list):
        bencode_string = ""
        for obj in py_obj:
            bencode_string += encode_bencode(obj).decode()
        return str(f"l{bencode_string}e").encode()
    if isinstance(py_obj, dict):
        bencode_string = ""
        for key, value in py_obj.items():
            bencode_string += encode_bencode(key).decode() + encode_bencode(value).decode()
        return str(f"d{bencode_string}e").encode()
        
def decode_bencode(bencoded_value):
    if chr(bencoded_value[0]).isdigit():
        first_colon_index = bencoded_value.find(b":")
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        
        length = int(bencoded_value[:first_colon_index])
        return bencoded_value[first_colon_index+1:first_colon_index+1+length]
    
    elif chr(bencoded_value[0]) == 'i':
        end_char = bencoded_value.find(b"e")
        if end_char == -1:
            raise ValueError("Invalid encoded value: No ending character 'e' found")    
        elif bencoded_value.find(b'0') == 1:
            raise ValueError("Invalid encoded value: No leading zeros allowed") 
        return int(bencoded_value[1:end_char])
    elif chr(bencoded_value[0]) == 'l': # list  
        decoded_list = []
        bencoded_value_copy = bencoded_value[1:]
        while bencoded_value_copy:
            if chr(bencoded_value_copy[0]) == 'e':
                return decoded_list
            decoded_list.append(decode_bencode(bencoded_value_copy))
            if isinstance(decoded_list[-1], int):
                entry_len = len(str(decoded_list[-1]))
            else:
                entry_len = len(decoded_list[-1])
            offset = 2
            if chr(bencoded_value_copy[0]).isdigit():
                offset = bencoded_value_copy.find(b':') + 1
            bencoded_value_copy = bencoded_value_copy[entry_len + offset:]
            
        return decoded_list
    elif chr(bencoded_value[0]) == 'd':
        decoded_dict = {}
        bencoded_value_copy = bencoded_value[1:]
        while bencoded_value_copy:
            if chr(bencoded_value_copy[0]) == 'e':
                return decoded_dict
            key = decode_bencode(bencoded_value_copy)
            offset = 2
            if chr(bencoded_value_copy[0]).isdigit():
                offset = bencoded_value_copy.find(b':') + 1
            # keys are always strings
            bencoded_value_copy = bencoded_value_copy[len(key) + offset:]
            # values can be strings, integers, lists or dicts
            value = decode_bencode(bencoded_value_copy)
            if isinstance(value, int):
                entry_len = len(str(value))
            elif isinstance(value, list):
                entry_len = list_elem_length(value)
            elif isinstance(value, dict):
                entry_len = dict_elem_length(value)
            else:
                entry_len = len(value)
            decoded_dict[key] = value
            bencoded_value_copy = bencoded_value_copy[entry_len + len(str(entry_len)) + 1:]
            
            
                                