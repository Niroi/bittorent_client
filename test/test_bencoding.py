import unittest
from app.bencoding import decode_bencode, encode_bencode

class TestBEncodingDecoding(unittest.TestCase):
    
    def test_string(self):
        bin_string = b'11:Hello World'
        result_string = decode_bencode(bin_string)
        assert result_string == b'Hello World'
        
    def test_string_len(sefl):
        bin_string = b'11:Hello World'
        result_string = decode_bencode(bin_string)
        assert len(result_string) is 11
    
    def test_string_empty(self):
        bin_string = b'0:Hello World'
        result_string = decode_bencode(bin_string)
        assert result_string == b"", f"{result_string=}"
    
    def test_string_no_colon(self):
        bin_string = b'11Hello World'
        with self.assertRaises(ValueError):
            decode_bencode(bin_string)
        
    def test_integer_positive(self):
        bin_integer = b'i123e'
        result_integer = decode_bencode(bin_integer)
        assert result_integer == 123, f"{result_integer} unequal 123"
        
    def test_integer_negative(self):
        bin_integer = b'i-123e'
        result_integer = decode_bencode(bin_integer)
        assert result_integer == -123, f"{result_integer} unequal -123"
        
    def test_integer_leading_zero(self):
        bin_integer = b'i0123e'
        with self.assertRaises(ValueError):
            decode_bencode(bin_integer)
    
    def test_integer_no_ending_e(self):
        bin_integer = b'i123'
        with self.assertRaises(ValueError):
            decode_bencode(bin_integer)
    
    def test_list_empty(self):
        bin_list = b'le'
        result_list = decode_bencode(bin_list)
        assert result_list == [], f"{result_list} unequal []"
    
    def test_list_integers(self):
        bin_list = b'li1ei2ei3ee'
        result_list = decode_bencode(bin_list)
        assert result_list == [1, 2, 3], f"{result_list} unequal [1, 2, 3]"
    
    def test_list_strings(self):
        bin_list = b'l5:apple5:banan4:pear4:kiwie'
        result_list = decode_bencode(bin_list)
        assert result_list == [b'apple', b'banan', b'pear', b'kiwi'], f"{result_list} unequal [b'apple', b'banan', b'pear', b'kiwi']"
    
    def test_nested_lists(self):
        bin_list = b'll11:Hello Worldi1eei42ee'
        exp_results = [[b'Hello World', 1], 42]
        result_list = decode_bencode(bin_list)    
        assert result_list == exp_results, f"{result_list} unequal {exp_results}"
        
    def test_dict_empty(self):
        bin_dict = b'de'
        result_dict = decode_bencode(bin_dict)
        assert result_dict == {}, f"{result_dict} unequal {{}}"
    
    def test_dict_string_keys(self):
        bin_dict = b'd3:bar4:spam3:fooi42ee'
        result_dict = decode_bencode(bin_dict)
        assert result_dict == {b'bar': b'spam',b'foo': 42}, f"{result_dict} unequal {{'bar': b'spam', 'foo': 42}}"
    
    def test_dict_integer_keys(self):
        bin_dict = b'di1ei2ei3ei4ee'
        with self.assertRaises(TypeError):
            decode_bencode(bin_dict)

class TestBencodingEncoding(unittest.TestCase):
    
    def test_string(self):
        string = "Hello World"
        bencoding = encode_bencode(string)
        assert bencoding == b'11:Hello World', f"{bencoding} unequal b'11:Hello World'"
    
    def test_integer(self):
        integer = 123
        bencoding = encode_bencode(integer)
        assert bencoding == b'i123e', f"{bencoding} unequal b'i123e'!"
        
    def test_list(self):
        arr = [1, 2, "Hello World"]
        exp_result = b'li1ei2e11:Hello Worlde'
        bencoding = encode_bencode(arr)
        assert bencoding == exp_result, f"{bencoding} unequal {exp_result}"
    
    def test_dict(self):
        hash_map = {
            "test1" : 1,
            "test2" : "2",
            "Hello" : "World",
        }
        exp_result = b'd5:test1i1e5:test21:25:Hello5:Worlde'
        bencoding = encode_bencode(hash_map)
        assert bencoding == exp_result, f"{bencoding} unequal {exp_result}"

class ResearchTests(unittest.TestCase):
    def test_UbuntuTorrent(self):
        with open('test/data/ubuntu-24.10-desktop-amd64.iso.torrent', 'rb') as f:
            meta_info = f.read()
            torrent = decode_bencode(meta_info)
        
        print(torrent)