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
from argparse import ArgumentParser

filename = 'AppleName.strings'
directory = '/System/Library/PrivateFrameworks/CoreEmoji.framework/Versions/A/Resources/en.lproj/'

def write_sbix_to_file():
    with open('out.xml', 'wb') as fx:
        mx = XMLWriter(fx)

        font = TTFont('Apple Color Emoji.ttc', fontNumber=1)
        bix = font['sbix']
        bix.toXML(xmlWriter=mx, ttFont=font)


def get_parsed_strings():
    with open(directory + filename, 'rb') as fp:
        reader = BPListReader(fp.read())
        parsed = reader.parse()
    return parsed

def extract_strikes_from_file(filename):
    sbix_table = ElementTree.parse(filename)
    strikes = sbix_table.findall('strike')
    return strikes


def extract_pngs_from_sbix_xml_file(filename):

    
    names = get_parsed_strings()

    strikes = extract_strikes_from_file(filename)

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

if __name__ == '__main__':

        parser = ArgumentParser(description='Extract PNG elements from TTF')
        parser.add_argument('-f','--ttc_file', help='ttc file', required=True)

        args = parser.parse_args()

        extract_strikes_from_file(args.ttc_file, "")

