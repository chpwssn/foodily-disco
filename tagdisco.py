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

version ="2"

recipes_done = set()
offsites_done = set()

parser = OptionParser()
parser.add_option("-p", dest="page", type="int",
                  help="The page number to pull from the api")
parser.add_option("-s", dest="size", type="int", default="1000",
                  help="The page size to pull from the api")
parser.add_option("-S", dest="term", default="*",
                  help="Search term")
parser.add_option("-F", dest="destfile",
                  help="Destination file")

(options, args) = parser.parse_args()

format = formatter.NullFormatter()
htmlparser = LinksExtractor(format)


url = "http://www.foodily.com/api/1/s/"+options.term+"?n="+str(options.size)+"&s="+str(options.page)

termforfile = re.sub(r'\*','star',options.term)

with open(options.destfile,"w") as logfile:
    print url
    data = urllib.urlopen(url)
    htmlparser.feed(data.read())
    htmlparser.close()
    links = htmlparser.get_links()
    for link in links:
        try:
            recipe = re.search(r'/r/(.+?)$',link).group(1)
            recipe = "recipe:"+recipe
            if recipe in recipes_done:
                recipe = ""
            else:
                recipes_done.add(recipe)
        except:
            recipe = ""
        if len(recipe) > 0:
            print recipe
            logfile.write(recipe+"\n")
        try:
            offsite = re.search(r'(https?://.+?)$',link).group(1)
            offsite = "offsite:"+offsite
            if offsite in offsites_done:
                offsite = ""
            else:
                offsites_done.add(offsite)
        except:
            offsite = ""
        if len(offsite) > 0:
            print offsite
            logfile.write(offsite+"\n")
time.sleep(1)
