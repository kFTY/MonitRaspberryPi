import urllib.request
import re
import time


def findblockheight():
    url = "https://www.btcforkmonitor.info/"
    try:
        urllib.request.urlretrieve(url, "info.txt")
    except:
        print ("error")
    outputfile = open("info.txt", "r", -1, 'utf-8').read()
    print (outputfile)
    # print (outputfile.read())

    blockheight = re.search(
        r"(Node: Bitcoin ABC)(.*)\n.*\n.*\n.*(height: )(\d{6})", outputfile).group(4)
    print (blockheight)
    return int(blockheight)


def push_to_phone(txt):
    txt = str(txt)
    os.system('/usr/bin/pushbullet.sh "%s" &> /dev/null' % txt)


blocktip = 0
while True:
    blockheight = findblockheight()
    if blockheight > blocktip:
        blocktip = blockheight
        push_to_phone("New BCC block %d" % blocktip)
    time.sleep(60)
