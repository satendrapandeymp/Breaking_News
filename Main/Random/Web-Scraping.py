import urllib2, time, sys, urllib, cookielib
from getpass import getpass
from bs4 import BeautifulSoup as Soup

reload(sys)
sys.setdefaultencoding("utf-8")

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')]

username = raw_input("username : ")
password = getpass()

opener.open('https://www.facebook.com/login')
login_data = urllib.urlencode({'email' : username, 'pass' : password})
opener.open('https://www.facebook.com/login', login_data)

#-------------------------------------------------------------------------------------------
# Done Authenticating till here
#--------------------------------------------------------------------------------------------


# posting on wall
def post_on_wall():

    person = raw_input("username of the person on which wall you want to post : ")

    test = opener.open('https://m.facebook.com/' + person)
    Page_Html = test.read()

    Parsed_html = Soup(Page_Html, "html.parser")
    form = Parsed_html.findAll("form")[1]
    inputs = form.findAll("input")

    message = raw_input("type message you want to post on his wall : ")
    data = {'xc_message' : message, 'view_post':'Post', 'rst_icv':''}
    data1 = data

    for i in range(8):
        data[str(inputs[i]['name'])] = str(inputs[i]['value'])

    link = 'https://m.facebook.com' + form['action']
    post_data = urllib.urlencode(data)
    test = opener.open(link, post_data)


# for comments details scrapping
def comment_scrape():

    id = raw_input("Type the page id : ")
    story_fbid = raw_input("Type the post id : ")

    seed = "https://m.facebook.com/story.php?story_fbid=" + str(story_fbid) + "&id=" + str(id)
    flag = 0

    File_name = "Data.csv"
    f = open(File_name, "w+")
    f.write("Name, Link, Comment, Likes \n")

    while flag == 0:
        response = opener.open(seed)
        Page_Html = response.read()
        Parsed_Html = Soup(Page_Html, "html.parser")

        more = 'see_next_' + str(story_fbid)
        try:
            Parsed_html = Parsed_Html.findAll("div", {"id":more})[0]
            key =  Parsed_html['class'][0]
            more_comment = Parsed_html.findAll("a")[0]
            seed = 'https://m.facebook.com' + more_comment['href']
        except:
            flag = 1

        if flag == 0:
            Parsed_htmls = Parsed_Html.findAll("div", {"class":key})
        else:
            Parsed_htmls = Parsed_Html.findAll("div", {"class":'do'}) + Parsed_Html.findAll("div", {"class":'dp'}) + Parsed_Html.findAll("div", {"class":'dh'})

        for Parsed_html in Parsed_htmls:
            try:
                Detail = Parsed_html.findAll("a")[0]
                name = Detail.text
                url = Detail['href']
                print url
                if '?id' in url:
                    url = url.split("&")[0]
                else:
                    url = url.split("?")[0]
                Comment = Parsed_html.findAll("div")[1].text.replace(',','-')
                Support = Parsed_html.findAll("div")[3]
                likes = Support.findAll("a")[0].text
                if likes == 'Like':
                    likes = str(0)
                f.write(name + ' , ' + url + ' , ' + Comment + ' , ' + likes + "\n")
            except:
                cool = 'cool'

    f.close()
