mini_printer
============

Creates a 4x6 printable image from images of creatures, as a substitute for
creature minis used in role playing games.

Usage:

    make_mini.py [ -h ] -i <url> [ -i <url> ... ] [ --l1=<text> ... ] <pattern>

Specify up to six images via a list of files or URLs using the -i command.
If an image has an exiv label, it will be used.  Otherwise, you need to use
the -ln option, where n=1-6.  Thus, each image is indexed (1-6).

<pattern> is a sequence of up to six numbers to represent which images will be
placed in the final image.

Example:

    make_mini.py -i kobold_trapmaster.png -i kobold_wildmage.jpg
        -i http://i.imgur.com/tXjq6.png -L3 "Kobold Rogue" 1 2 3 3 3

This creates a x 4x6 image with five pictures on it.  The first is
kobold_trapmaster.png.  The second is kobold_wildmage.jpg.  The remaining three
are all http://i.imgur.com/tXjq6.png.  The program assumes that
kobold_trapmaster.png and kobold_wildmage.jpg have exiv data with the name of
the image (e.g. "Kobold Trapmaster" and "Kobold Wildmage").  The third image
is taken directly from a website and given the label "Kobold Rogue".

You can add a label to the images themselves with the exiv2 command:

    #!/bin/sh
    FILE=$1
    shift
    exiv2 -M"del Exif.Image.ImageDescription" $FILE
    exiv2 -M"set Exif.Image.ImageDescription $*" $FILE

Example:

    label kobold_trapmaster.jpg Kobold Trapmaster


