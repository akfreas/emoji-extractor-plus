from bplist.bplist import BPListReader
from PIL import Image
from ipdb import set_trace as bp
import struct
import os
from io import BytesIO

filename = 'AppleName.strings'
directory = '/System/Library/PrivateFrameworks/CoreEmoji.framework/Versions/A/Resources/en.lproj/'


def extract_pngs_from_ttf():

    with open('/System/Library/Fonts/Apple Color Emoji.ttc', 'rb') as ttf:
        
        pos = 0
        png_seq = '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
        end_seq = '\x49\x45\x4E\x44'
        byte = ttf.read(8)
        current_png = None
         
        while byte:

            if current_png is None:
                
                byte = byte[1:]
                byte += ttf.read(1)
                if byte == png_seq:
                    current_png = byte
            if byte[:4] == end_seq:
                current_png += byte[-1]
                with open('test.png', 'wb') as png_file:
                    png_file.write(current_png)
                print('wrote file')
                os._exit(0)


            if current_png:
                lenword = ttf.read(4)
                length = struct.unpack('>I', lenword)[0]
                typ = ttf.read(4)
                data = ttf.read(length) if length > 0 else ''
                crc = ttf.read(4)

                current_png += lenword
                current_png += typ
                current_png += data
                current_png += crc

                if typ == 'IHDR':
                    width, height = struct.unpack('>II', data[:8])
                    bp()

                if typ == 'IEND':
                    bp()
                    current_png = None

                print('found more bytes', length, typ, ttf.tell())

with open(directory + filename, 'rb') as fp:
    reader = BPListReader(fp.read())
    parsed = reader.parse()
    bp()
    with open(filename + '_decoded.txt', 'w') as decoded:
        decoded.writelines(map(lambda x: x.encode('utf8'), parsed.keys()))
