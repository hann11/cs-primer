# Image Rotate

Given a .BMP file of bytes, want to rotate it.

Check out the [BMP file format](https://en.wikipedia.org/wiki/BMP_file_format) for more information.

The header of the BMP file contains information about the image, such as the width and height of the image, the number of bits per pixel, and the size of the image data.

E.g. the size of the image is at offset 2 and goes for 4 bytes. So we can parse that in Python as bytes[2:6].

We can get the offset where the pixels start at offset 10 for 4 bytes. So we can parse that in Python as bytes[10:14].

Note these are in little endian format, so we need to convert them to big endian.
