from fbchat import Client, log
from getpass import getpass
import time, os

username = 'satendrapandeymp'
password = '****'
client = Client(username, password)

time.sleep(2)

user = client.searchForUsers('Priyesh Jamra')[0]
message = "Hello meme"

time.sleep(2)

client.sendMessage(message, thread_id=user.uid)
