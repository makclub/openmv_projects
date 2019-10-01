#!/usr/bin/env python2.7
import sys, serial, struct, io
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

port = '/dev/tty.usbmodem0000000000111'
sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
             xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)

sp.setDTR(True) # dsrdtr is ignored on Windows.
plt_img = None
count = 0

while True:
    sp_bytes = sp.read(1)
    if (sp_bytes != b'I'):
        continue
    sp_bytes = sp.read(3)
    if (sp_bytes == b'MGS'):
        count = count + 1
        size = struct.unpack('<L', sp.read(4))[0]
        img = Image.open(io.BytesIO(sp.read(size)))
        if plt_img is None:
            plt_img = plt.imshow(np.array(img))
        else:
            plt_img.set_data(np.array(img))
        plt.pause(0.01)
        plt.draw()
        print(count)
