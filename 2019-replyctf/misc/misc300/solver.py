#!/usr/bin/env python3
from PIL import Image
import pytesseract  # install tesseract first -> brew install tesseract
                    # pip3 install pytesseract
import math
import re
import itertools
import string
import hashlib
import requests
import base64

url = "http://gamebox1.reply.it/ae6cdb9098e1252ec193b2c50587d1b3/"
session = requests.Session()
r = session.get(url)

print("Step 0 out of 5")
for i in range(5):
    # download image
    png_data = re.search('base64,(.+?)"', r.text).group(1)
    with open('image.png', 'wb') as f:
        f.write(base64.b64decode(png_data))

    im = Image.open('image.png')
    pixels = im.load()
    width, height = im.size # 640*480

    # get Green Plane 0
    # if LSB of green plane == 1 -> add a white pixel, black if not
    new_pixels = []
    for h in range(height):
        for w in range(width):
            if bin(pixels[w,h][1])[-1] == '1':
                new_pixels.append((255,255,255))
            else:
                new_pixels.append((0,0,0))

    out_img = Image.new(im.mode, im.size)
    out_img.putdata(new_pixels)
    out_img.save("equation.png", "PNG")

    # OCR
    equ = pytesseract.image_to_string(Image.open("equation.png"))
    print("Equation: " + equ)

    # get pixels from equation and create new image from it
    slope = float(re.search('y = floor \((.+?)x', equ).group(1))
    units = int(re.search('x(.+?)\)', equ).group(1).strip())

    new_pixels = []
    for x in range(width):
        y = math.floor(slope*x+units)
        px = im.getpixel((x,y))
        new_pixels.append(px)

    out_img = Image.new(im.mode, (width, 1))
    out_img.putdata(new_pixels)
    out_img.save("md5.png", "PNG")

    # extract MD5 from blue values
    md5sum = ""
    for j in range(32):
        md5sum += chr(new_pixels[j][2])
    print("CAPTCHA: " + md5sum)

    # send CAPTCHA
    data = {"response": md5sum}
    r = session.post(url, data=data)

    if i<4:
        # print steps to make sure captchas are passed
        print('\n' + re.search('<label>(.+?)</label>', r.text).group(1))
    else:
        # we passed the captchas so we save the new page
        print("\nCAPTCHA passed. New page exported to ./page.html!")
        with open('page.html', 'w') as f:
            f.write(r.text)

# get the last page
print("\nFetch page 58f5c08dd0131e49275cd553a9063131 content:")
url = "http://gamebox1.reply.it/ae6cdb9098e1252ec193b2c50587d1b3/58f5c08dd0131e49275cd553a9063131"
r = session.get(url)
print(r.text)