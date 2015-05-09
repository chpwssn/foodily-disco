import htmllib, formatter
import urllib, htmllib, formatter, re, time
from optparse import OptionParser

class LinksExtractor(htmllib.HTMLParser):
    
    def __init__(self, formatter):
        htmllib.HTMLParser.__init__(self, formatter)
        self.links = []
    
    def start_a(self, attrs):
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == "href":
                    self.links.append(attr[1])
    
    def get_links(self):
        return self.links

version ="1"

parser = OptionParser()
parser.add_option("-p", dest="page", type="int",
                  help="The page number to pull from the api")
parser.add_option("-s", dest="size", type="int", default="1000",
                  help="The page size to pull from the api")
parser.add_option("-S", dest="term",
                  help="Search term")

(options, args) = parser.parse_args()

format = formatter.NullFormatter()
htmlparser = LinksExtractor(format)


url = "http://www.foodily.com/api/1/s/"+options.term+"?n="+str(options.size)+"&s="+str(options.page)

termforfile = options.term
if options.term == "*":
    termforfile = "star"

with open(termforfile+"-"+str(options.size)+"-"+str(options.page)+"-"+str(int(time.time()))+"-"+version+"disco.txt","w") as logfile:
    print url
    data = urllib.urlopen(url)
    htmlparser.feed(data.read())
    htmlparser.close()
    links = htmlparser.get_links()
    for link in links:
        try:
            recipe = re.search(r'/r/(.+?)$',link).group(1)
            recipe = "recipe:"+recipe
        except:
            recipe = ""
        if len(recipe) > 0:
            print recipe
            logfile.write(recipe+"\n")
        try:
            offsite = re.search(r'(https?://.+?)$',link).group(1)
            offsite = "offsite:"+offsite
        except:
            offsite = ""
        if len(offsite) > 0:
            print offsite
            logfile.write(offsite+"\n")
time.sleep(1)
