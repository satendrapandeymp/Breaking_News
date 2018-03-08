import textwrap, smtplib
from twilio.rest import Client

# for sending message 
def sendMail(FROM,TO,SUBJECT,TEXT,SERVER, username, password):
    """this is some test documentation in the function"""
    message = textwrap.dedent("""\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT))
    # Send the mail
    server = smtplib.SMTP(SERVER)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(FROM, TO, message)
    server.quit()

FROM = "satyendra****@gmail.com"
TO = ["p****@iitk.ac.in"]
SUBJECT = "Testing"
TEXT = "Hi there, I'm just testing this thing"
SERVER = 'smtp.gmail.com:587'
username = "satend***"
pas = "******"
sendMail(FROM,TO,SUBJECT,TEXT,SERVER, username, pas)

# for sending the mail
def sendMessage(SID, Tocken, to ,from_ , body):
	client = Client(SID, Tocken)
	client.messages.create(to= to, from_ = from_, body= body)

to="+91737633****"
from_="+1415991****"
body="Hello from Python! This is a test :p"
SID = "ACed16c3e********"
Tocken = "dbb7c5f5*******"
sendMessage(SID, Tocken, to ,from_ , body)


