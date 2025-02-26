 #!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
# import mysql.connector
import Adafruit_CharLCD as LCD
import psycopg2
import yaml
import os
import sched
import threading

# done_counting = threading.Event()

# done_counting.wait(0.5)


CURRENT_DIR = os.path.dirname(__file__)

#import eink.py
with open("/home/pi/ranger_attendance/dbcreds.yml", 'r') as ymlfile:
    conf = yaml.load(ymlfile)
#conf = yaml.load(open('./dbcreds.yml'))
user = conf['User']
pwd = conf['Password']
host = conf['Host']
port = conf['Port']
database = conf['Database']
webhook_url = conf['Webhook']

db = psycopg2.connect(
  host=host,
  user=user,
  password=pwd,
  database=database,
  port=port
)

cursor = db.cursor()
reader = SimpleMFRC522()


### SCreen stuff
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype('/home/pi/ranger_attendance/chicago.ttf', 8)
fontsm = ImageFont.truetype('/home/pi/ranger_attendance/chicago.ttf', 6)
fontmd = ImageFont.truetype('/home/pi/ranger_attendance/chicago.ttf', 12)
fontlg = ImageFont.truetype('/home/pi/ranger_attendance/chicago.ttf', 18)
monaco = ImageFont.truetype('/home/pi/ranger_attendance/monaco.ttf', 12)

cairolg = ImageFont.truetype('/home/pi/ranger_attendance/Cairo.ttf', 18)
cairo = ImageFont.truetype('/home/pi/ranger_attendance/Cairo.ttf', 8)

x = 2

def clear():
  draw.rectangle((0, 0, width, height), outline=0, fill=0)

def header():
  draw.rectangle((0, 0, width, 10), outline=0, fill=1)
  #t = now.strftime("%H:%M")
  draw.text((1, 0), "Checkout  - Name", font=fontsm, fill=0)


def displayThanks():
  clear()
  textUsed = 'Thanks :) '
  turt = 'e'
  draw.text((x, top+8), textUsed, font=fontlg, fill=255)
  draw.text((x, top+8), turt, font=cairolg, fill=255)
  disp.image(image)
  disp.show()
  time.sleep(2)
  pass

def displayIn(name):
  clear()
  textUsed = 'Welcome '+ name
  draw.text((x, top+8), textUsed, font=font, fill=255)
  disp.image(image)
  disp.show()
  time.sleep(2)

  pass

def displayInfo(name):
  #clear()
  textUsed = 'Welcome '+ name
  draw.text((x, top+8), textUsed, font=font, fill=255)
  draw.rectangle((0, 0, width, 50), outline=1, fill=0)
  disp.image(image)
  disp.show()
  time.sleep(2)

  pass


def displayOut(name):
  clear()
  disp.image(image)
  textUsed = name
  g = 12
  for tex in name:
    draw.text((x, top+g), str(tex), font=font, fill=255)
    g +=10
  header()
  disp.image(image)
  disp.show()
  pass

def displayInvalidID():
  clear()
  textUsed = "YOU DIDN'T SAY \nTHE MAGIC WORD!"
  draw.text((x, top+8), textUsed, font=font, fill=255)
  disp.image(image)
  disp.show()
  pass

def displayInitName(name):
  #clear()
  textUsed = 'Please scan card for \n'+ name +'\n'
  draw.text((x, top+8), textUsed, font=font, fill=255)
  #draw.rectangle((0, 0, width, 50), outline=1, fill=0)
  disp.image(image)
  disp.show()
  #time.sleep(1)

  pass
### SEND EMAIL
import smtplib
def email(emailaddress):
  server = smtplib.SMTP('smtp.gmail.com', 587)

#Next, log in to the server
  server.login("ranger@urbanriv.org", "Theriverisdirty!!!")

#Send the mail
  msg = "Hello! /n You have been out for over 2 hours. Please confirm that you are indeed still out by replying to this message or by texting Ali. /n thanks, /n Ranger Rick the Robot" # The /n separates the message from the headers
  server.sendmail("ranger@urbanriv.org", emailaddress, msg)


# Posting to a Slack channel
def send_message_to_slack(text):
    import json
    import requests

    # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
    #webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {"text": "{0}".format(text)}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

    # from urllib import request, parse
    # import json
    #
    # post = {"text": "{0}".format(text)}
    #
    # try:
    #     json_data = json.dumps(post)
    #     req = request.Request("https://hooks.slack.com/services/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",
    #                           data=json_data.encode('ascii'),
    #                           headers={'Content-Type': 'application/json'})
    #     resp = request.urlopen(req)
    #
    # except Exception as em:
    #     print("EXCEPTION: " + str(em))
    #

def recentUsers():
  try:
    cursor.execute("Select first_name,last_name,phone,age(now(),clock_in),email, to_char(clock_in AT TIME ZONE 'America/Chicago', 'HH12:MI') as duration FROM attendance,users WHERE attendance.user_id = users.id AND attendance.clock_out IS NULL ORDER BY  duration DESC ;")
    result = cursor.fetchall()
    rout = []
    print(result)
    for x in result:
      pass
      g = days_hours_minutes(x[3])
      #m = x[0],x[1],'-H:',g[1],' M:',g[2]
      m = '{5} - {0} {1} '.format(x[0],x[1],x[2],g[1],g[2],x[5])
      print(x[0],x[1],x[2],'Time on water: ',g[1],' Hour',g[2],' Minutes ago', x[5])
      rout.append(''.join(str(m)))
      if g[1] > 2:
        #email(x[4]){0} {1}'.format(result[1],result[2])
        send_message_to_slack('@channel {0} {1} has been out for {3} Hour {4} Minutes. Phone: {2}'.format(x[0],x[1],x[2],g[1],g[2]))
    if cursor.rowcount >= 1:
      print(result[0][1])
      print(rout)
      displayOut(rout)
    pass
  finally:
    pass

#   cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

def userOutAlert(cursor):
  cursor.execute("Select user_id, age(clock_in) FROM attendance WHERE clock_out IS NULL ORDER BY clock_in")
  result = cursor.fetchall()
  print(result)
  displayOut(result)
  pass

def initializeCards():
  try:
    clear()
    cursor.execute("Select id, first_name,last_name,phone,email FROM users WHERE rfid_uid IS NULL;")
    result = cursor.fetchall()
    rout = []
    for x in result:
      #m = x[0],x[1],'-H:',g[1],' M:',g[2]
      m = '{1} {2} '.format(x[0],x[1],x[2],x[3])
      displayInitName(m)
      id, text = reader.read()
      cursor.execute("UPDATE users SET rfid_uid={} WHERE id= {}".format(str(id),x[0],))
      displayThanks()
    pass
  finally:
    pass


### start to check users in different thread
def startRecentUsersThread():
  while True:
    recentUsers()
    time.sleep(900)
    done_counting.set()

try:
  initializeCards()
  thread = threading.Thread(target=startRecentUsersThread)
  thread.start()
  while True:
    recentUsers()
    # lcd.clear()
    # lcd.message('Place Card to\nrecord attendance')
    id, text = reader.read()
    #id = 584185381670
    id = int(id)
    print(id)
    cursor.execute("Select id, first_name, last_name, phone FROM users WHERE rfid_uid=%s", (str(id),))
    result = cursor.fetchone()
    print(result)
#Check if account is valid, sign in or out the user.
    if cursor.rowcount >= 1:
      # lcd.message("Welcome " + result[1])
      cursor.execute("Select user_id FROM attendance WHERE clock_out IS NULL AND user_id= {}".format(result[0]))
      if cursor.rowcount >= 1:
        #currentUser = timeOut(cursor.fetchone())
        cursor.execute("UPDATE attendance SET clock_out=CURRENT_TIMESTAMP WHERE clock_out IS NULL AND user_id=(%s)", (result[0],))
        db.commit()
        print(result[1],result[2],' Checked out', result)
        send_message_to_slack('Checked Out: {0} {1}'.format(result[1],result[2]))
        displayThanks()
        recentUsers()

      else:
        cursor.execute("INSERT INTO attendance (user_id, clock_in) VALUES (%s, CURRENT_TIMESTAMP)", (result[0],) )
        print(result[1],result[2],' Checked in', result)
        db.commit()
        displayIn(str(result[1]))
        send_message_to_slack('Checked In: {0} {1}'.format(result[1],result[2]))
        recentUsers()
    else:
      displayInvalidID()
      time.sleep(1)
      initializeCards()

    #time.sleep(5)
finally:
  pass
  #GPIO.cleanup()
