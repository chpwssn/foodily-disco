from optparse import OptionParser

parser = OptionParser()
parser.add_option("-o", "--orig", dest="originals", type="int",
                  help="The number of originals pages the user has")
parser.add_option("-u", "--username", dest="username",
                  help="Username")
parser.add_option("-f", "--faves", dest="faves", type="int",
                  help="The number of faves pages the user has")

(options, args) = parser.parse_args()

with open("./"+options.username+"source.txt","w") as file:
	for x in xrange(options.originals+1):
		file.write("http://www.foodily.com/u/"+options.username+"?tab=originals&page="+str(x)+"\n")
	for x in xrange(options.faves+1):
		file.write("http://www.foodily.com/u/"+options.username+"?tab=faves&page="+str(x)+"\n")
