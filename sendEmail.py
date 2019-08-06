import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


def sendEmail(address)
# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
with open(textfile, 'rb') as fp:
    # Create a text/plain message
    msg = MIMEText(fp.read())

sendAddress = address + ', nick@urbanriv.org'

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'URGENT: are you on the water?'
msg['From'] = 'rangerBot@urbanriv.org'
msg['To'] = sendAddress
msg['Text'] = 'Hello! You are reciving this message because it looks like you have not clocked out from your ranger shift. If you are on the water please just reply to this email, if you forgot to clock out please reply as well. \n Thank you :)'

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail(me, [you], msg.as_string())
s.quit()