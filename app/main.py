import json
import sys

# import bencodepy - available if you need it!
# import requests - available if you need it!

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

# Examples:
#
# - decode_bencode(b"5:hello") -> b"hello"
# - decode_bencode(b"10:hello12345") -> b"hello12345"
def decode_bencode(bencoded_value):
    if chr(bencoded_value[0]).isdigit():
        first_colon_index = bencoded_value.find(b":")
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        
        length = int(bencoded_value.split(b":")[0])
        return bencoded_value[first_colon_index+1:first_colon_index+1+length]
    
    elif chr(bencoded_value[0]) == 'i':
        end_char = bencoded_value.find(b"e")
        if end_char == -1:
            raise ValueError("Invalid encoded value: No ending character 'e' found")    
        elif bencoded_value.find(b'0') == 1:
            raise ValueError("Invalid encoded value: No leading zeros allowed") 
        return int(bencoded_value[1:end_char])
    elif chr(bencoded_value[0]) == 'l' and chr(bencoded_value[-1]) == 'e': # list  
        decoded_list = []
        bencoded_value_copy = bencoded_value[1:-1]
        while bencoded_value_copy:
            decoded_list.append(decode_bencode(bencoded_value_copy))
            if isinstance(decoded_list[-1], int):
                entry_len = len(str(decoded_list[-1]))
            else:
                entry_len = len(decoded_list[-1])
            bencoded_value_copy = bencoded_value_copy[entry_len + 2:]
            # breakpoint()
        return decoded_list
    elif chr(bencoded_value[0]) == 'd' and chr(bencoded_value[-1]) == 'e':
        decoded_dict = {}
        bencoded_value_copy = bencoded_value[1:-1]
        while bencoded_value_copy:
            key = decode_bencode(bencoded_value_copy)
            # keys are always strings
            bencoded_value_copy = bencoded_value_copy[len(key) + 2:]
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
            decoded_dict[key.decode()] = value
            bencoded_value_copy = bencoded_value_copy[entry_len + 2:]
        return decoded_dict
        
def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        # Uncomment this block to pass the first stage
        print(json.dumps(decode_bencode(bencoded_value), default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
