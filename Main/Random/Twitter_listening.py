from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json, time, MySQLdb, sys

reload(sys)
sys.setdefaultencoding('utf-8')
arguments = sys.argv[1:]
keyword = " ".join(arguments)
print "your keyword is : ", keyword

conn = MySQLdb.connect("localhost","root","  ","chhaya")
c = conn.cursor()
conn.set_character_set('utf8')

ckey = "9VDSBBDXsXYRHlloCd*****"
csecret = "dmvLXOiv2Te4uMt***************5iLMhw6U"
atoken = "535319025-D3cirQ2QC5W5*********4V7clofALs"
asecret = "fXKoBQo8xJg1aSpQ*************9ARs3QIcQr"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

	try:
	    id = str(all_data["id"])
	    tweet = all_data["text"].encode('unicode_escape')
	    likes = str(all_data["favorite_count"])

	    if len(tweet) > 559:
		tweet = tweet[:558]

	    c.execute("INSERT INTO tweets (id, tweet, likes, keyword) VALUES (%s,%s,%s,%s)",(id, tweet, likes, keyword))
	    conn.commit()

	except KeyError:
	    return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[keyword])
