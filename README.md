# Emoji Extractor Plus ➕

Everyone 💕s Emojis. Problem is, it's hard to use them in Photoshop or in Google Slides and Docs. For this reason I created an emoji extractor that takes the PNG data from the Apple font and saves it as an image.


# Usage ⚒

* Clone this repo
* If you're using [virtualenv](https://virtualenv.pypa.io/en/stable/), make a new env
* Run `pip install -r requirements.pip`
* Run `python extract.py`

This will extract the PNGs from the font file at `/System/Library/Fonts/Apple Color Emoji.ttc`. If you want to target another font file, just use the `--ttc_file` flag with the path to the file.

The script will save the PNG data from the font into the `./images` directory wherever you ran the script. The following resolutions are curretly extracted:

160x160
96x96
64x64
52x52
48x48
40x40
32x32
26x26
20x20

All the emojis will be labeled with their proper names, too! 

![](https://s3.amazonaws.com/sashimiblade.com/emoji-files.png "")



# Fun Info

## Unicode is awesome 💥

Making this script was a fun exercise in learning more about Unicode and how it's being used to scale the number and types of emojis that Apple is making these days. With the addition of skin tones and gender modifiers, emoji are no longer one Unicode character anymore. 

To give an example of one of the more complicated emojis that Apple has created, take 👨‍👩‍👧‍👧, which comes from the Unicode string `\U0001f468\u200d\U0001f469\u200d\U0001f467\u200d\U0001f467`. (Shown as represented in Python)

This string is broken into several characters:

`\U0001f468`: 👱‍♂️
`\U0001f469`: 👩
`\U0001f467`: 👧

Each character has a `\u200d` character between it, which is a [zero width joiner](https://emojipedia.org/zero-width-joiner/) in between it. This character is used to join two or more Unicode characters together, in this case the people in the emoji. the ZWG is used also for any modifier, such as skin tone and gender.

My experience before this exercise was mostly with characters that were in the [ASCII table](https://www.asciitable.com/) from the olden days, so exploring this topic with emojis was interesting. Unicode was created to scale to many more characters than could be represented in the ASCII table, which allows it to support not only emojis, but all writing systems.
