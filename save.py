import os
import sys
import zlib
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print("Command line invalid.\nUsage: python", sys.argv[0], "d/e")
    quit()

mode = sys.argv[1]

if mode != "d" and mode != "e":
    print("Mode invalid. Must be 'd' for decrypt or 'e' for encrypt.\nUsage: python", sys.argv[0], "d/e")
    quit()   

char_map = [{"as": "a", "bs": "\xFC"}, {"as": "A", "bs": "\xDC"}, {"as": " ", "bs": "\xBD"}, {"as": "_", "bs": "\xC2"},
            {"as": "b", "bs": "\xFF"}, {"as": "B", "bs": "\xDF"}, {"as": "!", "bs": "\xBC"}, {"as": "\x0A", "bs": "\x97"},
            {"as": "c", "bs": "\xFE"}, {"as": "C", "bs": "\xDE"}, {"as": "\"", "bs": "\xBF"}, {"as": ",", "bs": "\xB1"},
            {"as": "d", "bs": "\xF9"}, {"as": "D", "bs": "\xD9"}, {"as": "$", "bs": "\xB9"}, {"as": ":", "bs": "\xA7"},
            {"as": "e", "bs": "\xF8"}, {"as": "E", "bs": "\xD8"}, {"as": "%", "bs": "\xB8"}, {"as": ";", "bs": "\xA6"},
            {"as": "f", "bs": "\xFB"}, {"as": "F", "bs": "\xDB"}, {"as": "-", "bs": "\xB0"}, {"as": "<", "bs": "\xA1"},
            {"as": "g", "bs": "\xFA"}, {"as": "G", "bs": "\xDA"}, {"as": ".", "bs": "\xB3"}, {"as": "=", "bs": "\xA0"},
            {"as": "h", "bs": "\xF5"}, {"as": "H", "bs": "\xD5"}, {"as": "/", "bs": "\xB2"}, {"as": ">", "bs": "\xA3"},
            {"as": "i", "bs": "\xF4"}, {"as": "I", "bs": "\xD4"}, {"as": "0", "bs": "\xAD"}, {"as": "[", "bs": "\xC6"},
            {"as": "j", "bs": "\xF7"}, {"as": "J", "bs": "\xD7"}, {"as": "1", "bs": "\xAC"}, {"as": "]", "bs": "\xC0"},
            {"as": "k", "bs": "\xF6"}, {"as": "K", "bs": "\xD6"}, {"as": "2", "bs": "\xAF"}, {"as": "W", "bs": "\xCA"},
            {"as": "l", "bs": "\xF1"}, {"as": "L", "bs": "\xD1"}, {"as": "3", "bs": "\xAE"}, {"as": "w", "bs": "\xEA"},
            {"as": "m", "bs": "\xF0"}, {"as": "M", "bs": "\xD0"}, {"as": "4", "bs": "\xA9"}, {"as": "v", "bs": "\xEB"},
            {"as": "n", "bs": "\xF3"}, {"as": "N", "bs": "\xD3"}, {"as": "5", "bs": "\xA8"}, {"as": "V", "bs": "\xCB"},
            {"as": "o", "bs": "\xF2"}, {"as": "O", "bs": "\xD2"}, {"as": "6", "bs": "\xAB"}, {"as": "u", "bs": "\xE8"},
            {"as": "p", "bs": "\xED"}, {"as": "P", "bs": "\xCD"}, {"as": "7", "bs": "\xAA"}, {"as": "U", "bs": "\xC8"},
            {"as": "q", "bs": "\xEC"}, {"as": "Q", "bs": "\xCC"}, {"as": "8", "bs": "\xA5"}, {"as": "x", "bs": "\xE5"},
            {"as": "r", "bs": "\xEF"}, {"as": "R", "bs": "\xCF"}, {"as": "9", "bs": "\xA4"}, {"as": "X", "bs": "\xC5"},
            {"as": "s", "bs": "\xEE"}, {"as": "S", "bs": "\xCE"}, {"as": "z", "bs": "\xE7"}, {"as": "Z", "bs": "\xC7"},
            {"as": "t", "bs": "\xE9"}, {"as": "T", "bs": "\xC9"}, {"as": "y", "bs": "\xE4"}, {"as": "Y", "bs": "\xC4"}]

char_dict = {}
for mapping in char_map:
    char_dict[mapping["as"]] = mapping["bs"]
    char_dict[mapping["bs"]] = mapping["as"]

folder_path = os.path.dirname(os.path.abspath(__file__))

if mode == "d":
    save_file = "save_data.xml"
    write_file = "plaintext.xml"
else:
    save_file = "plaintext.xml"
    write_file = "save_data.xml"
file_path = os.path.join(folder_path, save_file)

if not os.path.exists(file_path):
    print("Error:", save_file, "does not exist under the same directory.")
    quit()
if mode == "d":
    print("Decrypting 'save_data.xml' to 'plaintext.xml'...")
else:
    print("Encrypting 'plaintext.xml' to 'save_data.xml'...")

with open(save_file, "rb") as input_file:
    text = input_file.read()

output_data = bytearray()
for byte in text:
    char = chr(byte)
    if char in char_dict:
        output_data.append(ord(char_dict[char]))
    else:
        output_data.append(byte)
        print("Warning: Undocumented character", byte, ", left as-is.")

print("Extraction complete. Writing file...")
with open(write_file, "wb") as output_file:
    output_file.write(output_data)

print(write_file, "saved to the same directory.")

def file_crc32(filepath):
    crc = 0
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            crc = zlib.crc32(chunk, crc)
    return crc & 0xFFFFFFFF

save_data_path = os.path.join(folder_path, write_file)
if os.path.exists(save_data_path):
    crc = file_crc32(save_data_path)
    root = ET.Element("root")
    file_elem = ET.SubElement(root, "file")
    file_elem.set("name", "save_data.xml")
    file_elem.set("hash", str(crc))
    tree = ET.ElementTree(root)
    hash_file_path = os.path.join(folder_path, "save_hash.xml")
    tree.write(hash_file_path, encoding="utf-8", xml_declaration=True)
    print("CRC32 hash written to save_hash.xml.")
else:
    print("save_data.xml not found, skipping CRC32 hash generation.")
