import urllib.request
import re
import time
import os


def findblockheight():
    url = "https://www.btcforkmonitor.info/"
    try:
        urllib.request.urlretrieve(url, "info.txt")
    except:
        print ("error")
    outputfile = open("info.txt", "r", -1, 'utf-8')
    data = outputfile.read()
    blockheight = re.search(
        r"(Node: Bitcoin ABC)(.*)\n.*\n.*\n.*(height: )(\d{6})", data).group(4)
    outputfile.close()
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
