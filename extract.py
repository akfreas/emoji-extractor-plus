from bplist import BPListReader
from ipdb import set_trace as bp

filename = 'AppleName.strings'
directory = '/System/Library/PrivateFrameworks/CoreEmoji.framework/Versions/A/Resources/en.lproj/'


with open('/System/Library/Fonts/Apple Color Emoji.ttc') as ttf:
    bp()
    
    pos = 0
    byte = ttf.read(pos)
    while byte:
        pos += 1
        byte = ttf.read(pos)


with open(directory + filename, 'rb') as fp:
    reader = BPListReader(fp.read())
    parsed = reader.parse()
    with open(filename + '_decoded.txt', 'w') as decoded:
        decoded.writelines(map(lambda x: x.encode('utf8'), parsed.keys()))
