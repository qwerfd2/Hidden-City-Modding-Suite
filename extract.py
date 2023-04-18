import sys
import os
import traceback
import struct
import json

# This script is commented since I'm not happy with my implementation. It works but it is stupid. You're welcomed to improve its 
# performance and I will help you with the file structure.
#
#.v_sf follows the below structure:
#
# Header: 00 00 00 00 00 00 00 00 06 0E 00 00. first 8 bytes are 00 always, followed by file counts (0E 60 = 3680 files)
#
# Individual files: first file:
#30 52 00 00 38 00 00 00 //file length: 52 30, file type: 38 (unused)
#61 74 6C 61 73 5F 31 2E 70 6E 67 //filename: atlas_1.png
#00 00 00 00 //start offset: 00
#
#second file:
#A5 69 00 00 39 00 00 00 //file length: 69 A5, file type: 39
#61 74 6C 61 73 5F 31 30 2E 70 6E 67 //filename: atlas_10.png
#30 52 00 00 //start offset: 52 30
#
#After what I call "metadata", files are piled together according to the start offset and length. To sync the numbers up metadata must
#be removed.
#
#My implementation is slow because I need to manually check whether a file name has terminated using file extensions, since there is no 
#offseting, and some files have format like .xml.map, which necessitates looping. The game obviously doesn't do that, so improvements
#are definitely possible - maybe regex?
#
#Furthermore this implementation is more vulnerable to future changes - all file formats must be specified in "extensions" or else the 
#program crashes. A traverse limit of 150 bytes have been set to improve performance somewhat, but if the file name is longer than that
#it will also crash.


if len(sys.argv) < 3:
    print("Command line invalid.\nUsage: python", sys.argv[0], "pack.v_sf/all output_dir")
    quit()

file_name = sys.argv[1]
save_path = sys.argv[2]
if file_name[-5:] != '.v_sf' and file_name != 'all':
    print("Input file name invalid.\nUsage: python", sys.argv[0], "pack.v_sf/all output_dir")
    quit()

def extract(file_name):
    print("Opening", file_name, ".")
    
    #Use this to skip files already processed. temp.sav must be created, containing a [].

    #with open("temp.sav", 'r') as sa:
    #    processed = json.load(sa)
    #
    #if file_name in processed:
    #    print(file_name, "indicated as processed, skipping.")
    #    return

    try:
        with open(file_name, 'rb') as f:
            print(file_name, "opened.\nDetecting number of files.")
            f.read(8)
            file_c = struct.unpack('<I', f.read(4))[0]
            print(str(file_c),"file(s) detected.\nAcquiring file metadata.")
            data_bytes = f.read()
            index = 0
            file_count = 0

            #New file extensions must be added here.
            extensions = [".jpg", ".png", ".map", ".bin", ".xml", ".msk", "aaaaaa", ".lvl", ".mgcol", ".bat", "-1.png", ".txt", ".m3"]
            file_list = []
            file_len = len(data_bytes)
            while index < len(data_bytes):
                if file_count >= file_c:
                    break
                file_count += 1
                file_length = int(data_bytes[index:index+4][::-1].hex(), 16)
                
                #Unused.
                file_type = int(data_bytes[index+4:index+8][::-1].hex(), 16)
                index += 8
                filename = ""
                distance = []
                bound = 150
                if index + 150 > file_len:
                    bound = file_len - index
                for ext in extensions:
                    dist = data_bytes[index:index + bound].find(ext.encode('utf-8'))
                    if dist != -1:
                        distance.append({"ext": ext, "dist": dist})
                if distance:
                    distance = sorted(distance, key=lambda x: x["dist"])
                    for i in range(len(distance)):
                        if i == len(distance)-1 or distance[i+1]["dist"] > distance[i]["dist"] + len(distance[i]["ext"]):
                            filename = data_bytes[index:index+distance[i]["dist"]+len(distance[i]["ext"])].decode('ascii')
                            break
                if filename == "":
                    raise ValueError("Warning: Unknown file extension from", data_bytes[index:index+30].decode('utf-8'))

                start_offset = int(data_bytes[index+len(filename):index+4+len(filename)][::-1].hex(), 16)
                index += 4 + len(filename)
                file_object = {'name': filename, 'start': start_offset, 'length': file_length}
                #print(f"File {file_count}:")
                #print(f"file length: {file_length}, file type: {file_type}, file name: {filename}, start offset: {start_offset}")
                file_list.append(file_object)
            
            index += 12
            print("All file metadata acquired.\nExtracting file(s) to '", save_path, "' directory.")
            for file in file_list:
                #print("exporting", file)
                file_path = os.path.join(save_path, file["name"])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                f.seek(file['start'] + index)
                content = f.read(file['length'])
                with open(file_path, 'wb') as out:
                    out.write(content)

            print("All file(s) exported to '", save_path, "' directory.\n")

            #Again, uncomment this to record files already processed and skip them next time.
            #
            #processed.append(file_name)
            #with open("temp.sav", "w") as tempfile:
            #    tempfile.write(json.dumps(processed))


    except FileNotFoundError as e:
        print(file_name, "not found. Make sure it is in the same folder as the script itself. Traceback:\n", traceback.format_exc())
        quit()
    except ValueError as e:
        print(file_name, "is deformed - is it a Hidden City Hidden Mystery .v_sf file? Traceback:\n", traceback.format_exc())
        quit()
    except:
        print("An unknown error occurred at the step above. Traceback:\n", traceback.format_exc())
        quit()

if file_name == 'all':
    for file in os.listdir(os.path.dirname(__file__)):
        if file.endswith(".v_sf"):
            extract(file)
else:
    extract(file_name)
