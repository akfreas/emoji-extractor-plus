from bplist.bplist import BPListReader
from PIL import Image
import re
from ipdb import set_trace as bp
import struct
import os
from io import BytesIO
from fontTools.ttLib import TTFont
from fontTools.misc.xmlWriter import XMLWriter
from xml.etree import ElementTree

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

def write_sbix_to_file():
    with open('out.xml', 'wb') as fx:
        mx = XMLWriter(fx)

        font = TTFont('Apple Color Emoji.ttc', fontNumber=1)
        bix = font['sbix']
        bix.toXML(xmlWriter=mx, ttFont=font)


with open(directory + filename, 'rb') as fp:
    reader = BPListReader(fp.read())
    parsed = reader.parse()

sbix_table = ElementTree.parse('out.xml')
strikes = sbix_table.findall('strike')

for strike in strikes:

    for glyph in strike:

        name = glyph.attrib.get('name')
        if name:
            print name
        png_hexdata = glyph.find('hexdata')
        if png_hexdata is None:
            continue
        png_data = re.sub('[\\n\s]', '', png_hexdata.text).decode('hex')
        png_image = Image.open(BytesIO(png_data))
        hex_code = name.split('_')[-1]
        bp()
        image_filename = "{}_{}x{}.png".format(
            hex_code,
            png_image.size[0], 
            png_image.size[1]
        )
        png_image.save(os.path.join('./images/', image_filename))
        print('saved {}'.format(image_filename))

