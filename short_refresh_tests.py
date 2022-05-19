#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
picdir = "/home/pi/src/pic/"   #os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = "home/pi/src/lib/"   #os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import time
import traceback
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd2in9_V2 as epdmod


font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


def main():
    epd = epdmod.EPD()
    epd.init()
    epd.Clear(0xFF)
    mon_image = Image.new('1', (epd.height, epd.width), 255)
    mon_draw = ImageDraw.Draw(mon_image)

    #cycle
    i = 0
    refr = 0
    pwr_in = 650
    flow = 53
    d_flow = 10000
    mon_image = Image.new('1', (epd.height, epd.width), 255)
    mon_draw = ImageDraw.Draw(mon_image)
    faults = ["No fault", "You win X$"]
    fault = 0

    for i in range(5000):
        lineone = "Power: {} W".format(pwr_in)
        linetwo = "Flow: {} LPM".format(flow)
        linethree = "Daily Flow: {} L".format(d_flow)

        mon_draw.rectangle((10, 10, 280, 120), fill=255)  #clearing
        mon_draw.text((10, 0), 'SMPP Monitoring', font=font24, fill=0)
        mon_draw.text((10, 30), lineone, font=font18, fill=0)
        mon_draw.text((10, 50), linetwo, font=font18, fill=0)
        mon_draw.text((10, 70), linethree, font=font18, fill=0)
        mon_draw.text((10, 90), "Fault Status: {}".format(faults[fault]), font=font18, fill=0)
        newimage = mon_image.crop([10, 10, 120, 50])
        mon_image.paste(newimage, (10, 10))
        print("pre display")
        pre = datetime.now()
        epd.display(epd.getbuffer(mon_image))
        print("+{:2.1f} secs: pre sleep".format((datetime.now() - pre).total_seconds()))
        time.sleep(1)

        # simulate some change to the text
        fault = 1 - fault
        pwr_in = pwr_in + 13 if pwr_in + 13 <= 1500 else 300
        flow = flow + 2 if flow + 2 <= 70 else 20
        d_flow += 1

    epd.sleep()
    epd.Dev_exit()


if __name__ == '__main__':
    main()
