from urllib2 import urlopen
import urllib2

city="London" #we need to be careful about the wiki url

headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}    #Bypasses the bot-block from the site
req = urllib2.Request("http://en.wikipedia.org/wiki/"+city, headers=headers)
page=urllib2.urlopen(req).read()   #reades the whole webpage including the html





def keyword(variable):
    matches=page.count(variable)
    print matches
    
def switch(n):
    if n==1:
        keyword("beach")
    if n==2:
        keyword("desert")
    if n==3:
        keyword("mountain")
    if n==4:
        keyword("snow")
    if n==5:
        keyword("ancient")
    if n==6:
        keyword("island")
    

switch(6)
