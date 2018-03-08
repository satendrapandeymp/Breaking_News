import urllib2, urllib, os, random, cookielib, time, sys, ssl, HTMLParser, pdfkit
from bs4 import BeautifulSoup as Soup
from selenium import webdriver

# list to find useful section
parse_list = ['story-details', 'story-section', 'story-content', 'article-body section', 'article-section', 'article-full-content' ]

# Making utf-8 default encoding
reload(sys)
sys.setdefaultencoding("utf-8")

# Avoiding SSL problems
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# creating headers
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Connection': 'keep-alive',}

# creating build_opener
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [headers]

# loading selenium build_opener
for key in headers:
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
browser = webdriver.PhantomJS()

# fetch news from google
def google_links(page):
    res = []
    browser.get(page)
    time.sleep(2)
    #for _ in range(5):
     #   browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      #  time.sleep(2)
    Page_Html = browser.page_source

    '''
    with open("temp.html", 'w') as file:
        file.write(Page_Html)
    '''

    Parsed_html = Soup(Page_Html, "html.parser")
    Container = Parsed_html.findAll("div", {"id":"rso"})[0]
    rows = Container.findAll("div", {"class":"g"})

    for row in rows:
	try:
	    link = row.findAll("a")[0]['href']
	    original = link
	    link = link.replace("%3A", ":")
	    link = link.replace("%2F", "/")
	    link = link.replace("%2520", "%20")
	    res.append(link)
	except:
	    print "Found something not captured"

    return res


def download(name, arr, num):
	count = 0
	for doc in arr:
	    count += 1
	    link = doc
	    filename = link.split("://")[1].split("/")[0]
	    news_agency = filename
	    filename = filename + "_" + str(random.randint(1,9999)) + ".html"
	    file_name = "../satendrapandeymp.github.io/News/" + filename
	    try:
		test = opener.open(link, timeout=5)
		Page_Html = test.read()
		Parsed_html = Soup(Page_Html, "html.parser")
		title = Parsed_html.findAll("h1")[0].text
		for elem in parse_list:

		    try:
			Container = Parsed_html.findAll("div", {"class":elem})[0]
			print "Sucessfull now"
			Page_Html = Container
			break
		    except:
			continue
		    
		with open("../satendrapandeymp.github.io/News/template.html", 'r') as file:
		    template = file.read()	

		with open(file_name, 'wb') as file:
		    file.write(template.split("<!--Heading-->")[0] + str(title))
		    file.write(template.split("<!--Heading-->")[1].split("<!--Detail-->")[0]  + str(Page_Html) + template.split("<!--Heading-->")[1].split("<!--Detail-->")[1])		
	    
		# Updating News links
		with open("../satendrapandeymp.github.io/news.html", 'r') as file:
		    news_template = file.read()	

		with open("../satendrapandeymp.github.io/news.html", 'wb') as file:
		    temp_news = news_template.split("<!--Breking_news-->")
		    temp_link = temp_news[1].split("sample.html")[1]
		    file.write( temp_news[0] + "<!--Breking_news-->" + temp_news[1] + "<!--Breking_news-->"   + temp_news[1].split("sample.html")[0] + filename + temp_link.split("sample")[0] + news_agency + "_on_"  + "_".join(name.split(' ')) + temp_link.split("sample")[1] + temp_news[2])
		     
	    except:
		    print link
	    
	    if count > num:
		break

check =raw_input('Do you have urls.txt ? y/n : ')

if check.lower() == 'y':
    seed=raw_input('Meks sure your filename is in this format -: \nurl1\nurl2\n...\nEnter PATH to Filename : ')
    file = open(seed, 'r')
    result = file.read().split('\n')
    num = len(result)
    num = 2
    seed = seed.split(".")[0]

else:
	seed=raw_input('Enter the keywords : ')
	num=int(raw_input('No of News you want -- : '))
	query = "https://www.google.co.in/search?num=100&client=ubuntu&hs=RWy&channel=fs&dcr=0&source=lnms&tbm=nws&sa=X&ved=0ahUKEwjAr5-vjcHZAhUMsI8KHe_3DSkQ_AUICigB&biw=1366&bih=662&q=" + "+".join(seed.split(' '))
	result = google_links(query)

	'''
	with open(seed+".txt", 'wb') as writer:
	    for url in result:
		writer.write(url + "\n")
	'''	

download(seed, result, num)

# Pdf Parts
#pdfkit.from_url('http://google.com', 'out.pdf')

os.remove("ghostdriver.log")

os.system("bash auto_push.sh")

