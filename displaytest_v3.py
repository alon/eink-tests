#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
picdir = "/home/pi/src/pic/"   #os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = "home/pi/src/lib/"   #os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in9
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    epd.init(epd.lut_partial_update)
    mon_image = Image.new('1', (epd.height, epd.width), 255)
    mon_draw = ImageDraw.Draw(mon_image)
except:
    print("Display Error")

time.sleep(1)

#cycle
i = 0
refr = 0
pwr_in = 650
flow = 53
d_flow = 10000
pwr_in = str(pwr_in)
flow = str(flow)
d_flow = str(d_flow)

while i < 5000:
    if refr > 3:
        try:
            epd = epd2in9.EPD()
            epd.init(epd.lut_full_update)
            epd.Clear(0xFF)
            font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
            font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
            epd.init(epd.lut_partial_update)
            mon_image = Image.new('1', (epd.height, epd.width), 255)
            mon_draw = ImageDraw.Draw(mon_image)
            refr = 0
        except:
            print("Regular Refresh Error")


    lineone = "Power: " + pwr_in + " W"
    linetwo = "Flow: " + flow + " LPM"
    linethree = "Daily Flow: " + d_flow + "L"
    try:
        mon_draw.rectangle((10, 10, 280, 120), fill = 255)  #clearing
        mon_draw.text((10, 0), 'SMPP Monitoring', font = font24, fill = 0)
        mon_draw.text((10, 30), lineone, font = font18, fill = 0)
        mon_draw.text((10, 50), linetwo, font = font18, fill = 0)
        mon_draw.text((10, 70), linethree, font = font18, fill = 0)
        mon_draw.text((10, 90), "Fault Status: No fault", font = font18, fill = 0)       
        newimage = mon_image.crop([10, 10, 120, 50])
        mon_image.paste(newimage, (10,10))
        epd.display(epd.getbuffer(mon_image))
        time.sleep(2)
    except:
        print("loop error")

    pwr_in = int(pwr_in)
    pwr_in += 13
    if pwr_in > 1500:
        pwr_in = 300

    pwr_in = str(pwr_in)
    flow = int(flow)
    flow += 2
    if flow > 70:
        flow = 20
    flow = str(flow)
    d_flow = int(d_flow)
    d_flow += 1
    d_flow = str(d_flow)
    i += 1
    refr += 1

epd.sleep()
epd.Dev_exit()

#except IOError as e:
#    logging.info(e)

#except KeyboardInterrupt:
#    logging.info("ctrl + c:")
#    epd2in9.epdconfig.module_exit()
#    exit()
