import time, MySQLdb, sys, tweepy

reload(sys)
sys.setdefaultencoding('utf-8')

ckey = "9VDSBBD**********drH6612O"
csecret = "dmvLXOiv2Te4uMtu6x85***********"
atoken = "535319025-D3cirQ2QC5W5Epe7m5G1G5MVRDB8Cq********"
asecret = "fXKoBQo8xJg1aSpQ************kmA9ARs3QIc"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

tweet =  api.user_timeline("republic")[0]
id = str(tweet.id)
text = tweet.text
likes = tweet.favorite_count

print "https://twitter.com/test/status/" + id
print text
print likes
