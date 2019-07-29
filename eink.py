
#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append(r'../lib')

import epd7in5bc
import epdconfig
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


def displayUser(Usernames):

    try:
        print("epd7in5bc Demo")
        
        epd = epd7in5bc.EPD()
        print("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)
        
        # Drawing on the image
        print("Drawing")
        font36 = ImageFont.truetype('../lib/Font.ttc', 36)
        font24 = ImageFont.truetype('../lib/Font.ttc', 24)
        font18 = ImageFont.truetype('../lib/Font.ttc', 18)
        # Drawing on the Horizontal image
        print("1.Drawing on the Horizontal image...") 
        HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126
        HRYimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126  ryimage: red or yellow image  
        drawblack = ImageDraw.Draw(HBlackimage)
        drawry = ImageDraw.Draw(HRYimage)
        
        # Standard box sections
        uSection = 10
        uSectionTime = 60

        numUsers = 0
        for userOut in usernames:
            place = uSection + (numUsers*10)
            userOutPrint = userOut[1] +' '+userOut[2]+' Phone: '+userOut[3]
            #TODO: find out how many in list, add logic for if user is still out
            userTimePrint= userOut[4]
            drawblack.text((place, 0), str(userTimePrint), font = font24, fill = 0)
            drawry.text((place, uSectionTime), str(userOutPrint), font = font24, fill = 0)

        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        time.sleep(2)
        
        
        print("Goto Sleep...")
        epd.sleep()
            
    except IOError as e:
        print(e)
        
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epdconfig.module_exit()
        exit()
    pass