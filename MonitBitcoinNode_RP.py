from subprocess import check_output
from subprocess import CalledProcessError
import os
import urllib.request
from time import sleep, strftime
from tendo import singleton
me = singleton.SingleInstance()

stat = ""
upgrade = False
print (strftime("%Y-%m-%d %H:%M:%S"))


def upgradedev():
    print ("Start to pull from Github.com")
    try:
        os.system("bitcoin-cli stop")
    except:
        print ("API not answering.")
    try:
        print ("Starting autogen")
    except CalledProcessError as e:
        print(e.output)
    try:
        print (check_output("/home/pi/buildgit/bu-dev/autogen.sh",
                            shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    print ("Starting config")
    try:
        print (check_output(
            "/home/pi/buildgit/bu-dev/configure --disable-wallet --without-gui", shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    sleep(5)
    print ("Starting make")
    try:
        print (check_output("make", shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    # not sure if we need a directory setting here,
    #  "make --directory=/home/pi/buildgit/bu-dev/")
    sleep(5)
    print ("Starting install")
    # not sure if we need a directory setting here,
    try:
        print (check_output("sudo make install", shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    print ("Starting strip")
    try:
        print (check_output("sudo strip bitcoind", shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    try:
        print (check_output("sudo strip bitcoin-cli", shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    try:
        print (check_output(
            '/usr/bin/pushbullet.sh "New version of dev installed"', shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    # try:
    #    print (check_output("sudo reboot", shell=True).decode("UTF-8"))
    # except CalledProcessError as e:
    #    print(e.output)


def get_info():
    try:
        return(check_output("bitcoin-cli getinfo", shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        error = e.output
        if error.find("code") == -1:
            error = "error"
        return (error)


def get_mempool():
    try:
        return(check_output("bitcoin-cli getmempoolinfo", shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        error = e.output
        if error.find("code") == -1:
            error = "error"
        return (error)


def push_to_phone(txt):
    txt = str(txt)
    os.system('/usr/bin/pushbullet.sh "%s"' % txt)


def checkstat():
    # get height of the latest block from btc.com
    apiReadout = str(urllib.request.urlopen(
        'https://chain.api.btc.com/v3/block/latest').read())
    blockNumber = int(apiReadout[apiReadout.find(
        "height") + 8:apiReadout.find("height") + 14])
    # get height of the latest block from bitcoin-cli
    info = str(get_info())
    print (info)

    if info == "error":
        stat = "Bitcoin node restarting"
        push_to_phone(stat)
        print (stat)
        os.system(
            'cp -f /home/pi/DV3/Coin/debug.log /home/pi/DV3/Coin/debug.log.bak')
        os.system('sudo reboot')

    if info.find("version") != -1:
    	blockNumberCli = int(
        	info[info.find("blocks") + 9:info.find("blocks") + 15])
# in case fail: notify me
# if running but off-sync over 3 blocks:
    	diff = blockNumberCli - blockNumber
	    if diff > 3:
	        stat = "Bitcoin node offSync %i blocks" % diff
	        push_to_phone(stat)
	        print (stat)
	    else:
	        stat = "Bitcoin node Running OK, offset %i block" % diff
	        print (stat)
# if bitcoin-cli is not responsing:
    


# Upgrade time?
isupgradeTime = int(strftime("%H")) == 2
if isupgradeTime:
    isnewVersion = str(check_output(
        "git -C /home/pi/buildgit/bu-dev pull", shell=True).decode("UTF-8")).find("up-to-date") == -1

if isupgradeTime and isnewVersion:
    upgrade = True
    #print ("upgrade start")

if isupgradeTime and (not upnewVersion):
    upgrade = False
    print ("Nothing new, abort upgrade")

if upgrade:
   # upgradedev()
    checkstat()
else:
    checkstat()
