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

import codecs


def exit():
    os._exit(0)

def write_sbix_to_file(filename):

    out_filename = filename.replace(' ', '_') + '.xml'

    if os.path.exists(out_filename):
        print('%s already exists. not extracting' % out_filename)
        return out_filename

    print('extracting sbix chunk to file %s' % out_filename)

    with open(out_filename, 'wb') as fx:
        mx = XMLWriter(fx)
        mx.begintag("root")

        font = TTFont(filename, fontNumber=1)
        bix = font['sbix']
        bix.toXML(xmlWriter=mx, ttFont=font)
        mx.endtag("root")
        mx.close()
    return out_filename


def get_parsed_strings():

    filename = 'AppleName.strings'
    directory = '/System/Library/PrivateFrameworks/CoreEmoji.framework/Versions/A/Resources/en.lproj/'

    with open(directory + filename, 'rb') as fp:
        reader = BPListReader(fp.read())
        parsed = reader.parse()

    new_parsed = parsed.copy()
    for key in parsed:
        graphical_key = key.replace(u'\ufe0f', u'').replace(u'\u20E3', u'').replace(u'\u200d', '')
        new_parsed[graphical_key] = parsed[key]


    return new_parsed

def extract_strikes_from_file(filename):
    sbix_table = ElementTree.parse(filename)
    strikes = sbix_table.findall('strike')
    return strikes


def escaped_string_from_string(string):
    
    hex_code = string.replace('u', '')
    number = int(hex_code, 16)
    return '\\U{:0>8X}'.format(number)

def extract_pngs_from_sbix_xml_file(filename):

    
    names = get_parsed_strings()

    strikes = extract_strikes_from_file(filename)

    created_dirs_for_sizes = []

    modifier_matcher = re.compile(r'\.(?P<skin_tone>[0-5]{0,1})?\.?(?P<gender>[MWBG]{0,4})?')
    matcher = re.compile(r'([A-F0-9]{4,8})')

    for strike in strikes:

        for glyph in strike:
            gender = None
            skin_tone = None
            glyph_codes = glyph.attrib.get('name')

            png_hexdata = glyph.find('hexdata')
            if png_hexdata is None:
                continue
            png_data = re.sub('[\\n\s]', '', png_hexdata.text).decode('hex')
            png_image = Image.open(BytesIO(png_data))
            modifiers = modifier_matcher.search(glyph_codes)
            codes = matcher.findall(glyph_codes)
            if codes is None:
                continue
            if modifiers is not None:
                mod_dict = modifiers.groupdict()
                gender = mod_dict['gender']
                skin_tone = mod_dict['skin_tone']

            key_string = u''
            for code in codes:
                if u'fe0f' in code or u'20E3' in code:
                    continue
                key_string += escaped_string_from_string(code)
            
            decoded = codecs.decode(key_string,'unicode-escape')

            if gender == 'W':
                decoded += u'\u2640'
                gender = None
            elif gender == 'M':
                decoded += u'\u2642'
                gender = None



            try:
                name = names[decoded].replace('/', ' ')
            except KeyError:
                print(u'no name found for {} ({})'.format(decoded, key_string))
                name = glyph.attrib.get('name')

            image_dir = os.path.join('./images', "{}x{}".format(
                png_image.size[0], 
                png_image.size[1]
            ))
            if image_dir not in created_dirs_for_sizes:
                created_dirs_for_sizes += image_dir
                if os.path.exists(image_dir) == False:
                    os.mkdir(image_dir)
                    created_dirs_for_sizes += image_dir

            image_filename = name 

            if gender:
                image_filename += u' {}'.format(gender.lower())
            if skin_tone:
                image_filename += u' {}'.format(skin_tone)

            image_filename += u'.png'
                

            png_image.save(os.path.join(image_dir, image_filename))
            print(u'saved {}/{}'.format(image_dir, image_filename))

if __name__ == '__main__':

        parser = ArgumentParser(description='Extract PNG elements from TTF')
        parser.add_argument('-f','--ttc_file', help='ttc file', required=True)

        args = parser.parse_args()

        sbix = write_sbix_to_file(args.ttc_file)
        extract_pngs_from_sbix_xml_file(sbix)
        #strikes = extract_strikes_from_file(args.ttc_file)
        parsed = get_parsed_strings()

