 #!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
# import mysql.connector
# import Adafruit_CharLCD as LCD
import psycopg2
import yaml

#import eink.py

conf = yaml.load(open('dbcreds.yml'))
user = conf['User']
pwd = conf['Password']
host = conf['Host']
port = conf['Port']
database = conf['Database']

db = psycopg2.connect(
  host=host,
  user=user,
  password=pwd,
  database=database,
  port=port 
)

cursor = db.cursor()
reader = SimpleMFRC522()


try:
  while True:
    # lcd.clear()
    # lcd.message('Place Card to\nrecord attendance')
    id, text = reader.read()
    print(id)
    cursor.execute("Select id, firstName, lastName, phone FROM users WHERE rfid_uid=(%s)", (id))
    result = cursor.fetchone()
    print(result)
#Check if account is valid, sign in or out the user.
    if cursor.rowcount >= 1:
      # lcd.message("Welcome " + result[1])
      cursor.execute("Select user_id FROM attendance WHERE time_out IS NULL")
      if cursor.rowcount >= 1:
        currentUser = timeOut(cursor.fetchone())
        cursor.execute("UPDATE attendance SET time_out=CURRENT_TIMESTAMP WHERE time_out IS_NULL AND user_id=(%s)", (result[0],))
        db.commit()
        print(result[1],result[2],' Checked out')
      else:
        cursor.execute("INSERT INTO attendance (user_id, time_in) VALUES (%s, CURRENT_TIMESTAMP)", (result[0],) )
        print(result[1],result[2],' Checked in')
        db.commit()                                                                                                                                                    .message("User does not exist.")
    time.sleep(2)
finally:
  GPIO.cleanup()

# def recentUsers():
#   try:
#     cursor.execute("Select user_id, firstName, lastName, phone FROM attendance WHERE time_out IS NULL ORDER BY time_in ")
#     result = cursor.fetch()
#     print(result)
#     if cursor.rowcount >= 1:
#       displayUser(Usernames)
#     pass

# def userOutAlert():
#   try:
#     cursor.execute("Select user_id, firstName, lastName, phone FROM attendance WHERE time_out IS NULL ORDER BY time_in ")
#     result = cursor.fetch()
#     print(result)  
#     pass

# def timeOut():
#   try:
#   t = psycopg2.Timestamp  
#   cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )

