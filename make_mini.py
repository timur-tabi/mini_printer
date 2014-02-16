#!/usr/bin/env python

# Copyright 2013, Timur Tabi
# Licensed under the GPL v3.  See file LICENSE for information.

# This program takes one or more images of creatures and converts them into a
# montage that can be printed on 4x6 photo paper.  The individual creatures can
# be cut out and folded to make stand-up minis used in role playing games.

# This program requires ImageMagick and the Wand Python
# package (http://wand-py.org).

import sys
import os

# Use the standard Mac python package
os.environ['MAGICK_HOME']='/opt/local'

from urllib2 import urlopen
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
from optparse import OptionParser, OptionGroup

# Prevent optparse from stripping newlines from the epilog
# OptionParser.format_epilog = lambda self, formatter: self.epilog

parser = OptionParser(usage="usage: %prog [options] pattern")

parser.add_option("-i", dest="urls", help="list of images", action="append")
parser.add_option("--l1", dest="l1", help="label for image 1", default=None)
parser.add_option("--l2", dest="l2", help="label for image 2", default=None)
parser.add_option("--l3", dest="l3", help="label for image 3", default=None)
parser.add_option("--l4", dest="l4", help="label for image 4", default=None)
parser.add_option("--l5", dest="l5", help="label for image 5", default=None)
parser.add_option("--l6", dest="l6", help="label for image 6", default=None)

(options, args) = parser.parse_args()

image = Image(width=6*300, height = 2*600, background=Color('white'), resolution=(300,300))
labels = [options.l1, options.l2, options.l3, options.l4, options.l5, options.l6]

print labels
print options.urls
print args

for index, pos in enumerate(args):
    pos = int(pos) - 1
    url = options.urls[pos]
    print url
    try:
        f = open(url)
    except:
        f = urlopen(url)

    # Create a blank canvas of the right size
    img = Image(width=300, height=600, background=Color('white'),
        resolution=(300,300))

    # Overlay the image we asked for
    with Image(file=f) as loaded:
        loaded.transform('', '300')
        if loaded.height > 410:
            loaded.crop(0, 0, 300, 410)
        if 'exif:ImageDescription' in loaded.metadata:
            label = loaded.metadata['exif:ImageDescription']
        img.composite(loaded, 0, 0)

    # TODO: use img.caption() instead
    with Drawing() as draw:
        draw.stroke_color = Color('black')
        draw.font = 'Arial Narrow'
        draw.font_size = 24
        draw.text_alignment = 'center'
        draw.text(img.width / 2, 450, label)
        draw(img)

    # convert $1 -fill '#0008' -draw 'rectangle 5,420,295,450' -fill white
    # -undercolor none -pointsize 24 -gravity South -annotate +0+10 " $2 " $1

    image.composite(img, index * 300, 600)
    img.rotate(180)
    image.composite(img, index * 300, 0)

#            print img.metadata.items()
#            print img.size

image.format = 'png'
display(image)
#image.save(filename='/tmp/image.png')