from bplist.bplist import BPListReader
from PIL import Image
from ipdb import set_trace as bp

filename = 'AppleName.strings'
directory = '/System/Library/PrivateFrameworks/CoreEmoji.framework/Versions/A/Resources/en.lproj/'


with open('/System/Library/Fonts/Apple Color Emoji.ttc', 'rb') as ttf:
    
    pos = 0
    png_seq = '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    end_seq = '\x49\x45\x4E\x44'
    byte = ttf.read(8)
    current_png = None
     
    while byte:

        if byte == png_seq:
            current_png = byte
            print('found png')
        if current_png:
            current_png += byte
            print('found more bytes')
        if byte[:4] == end_seq:
            current_png += byte
            with open('test.png', 'wb') as png_file:
                png_file.write(current_png)
            bp()
            print('wrote file')
            import os
            os._exit(0)
        pos += 1
        ttf.seek(pos)
        byte = byte[1:]
        byte += ttf.read(1)

with open(directory + filename, 'rb') as fp:
    reader = BPListReader(fp.read())
    parsed = reader.parse()
    bp()
    with open(filename + '_decoded.txt', 'w') as decoded:
        decoded.writelines(map(lambda x: x.encode('utf8'), parsed.keys()))
