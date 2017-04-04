from subprocess import check_output
from subprocess import CalledProcessError
import os
import urllib2
from time import strftime
from tendo import singleton
me = singleton.SingleInstance()

# Initialize
print (strftime("%Y-%m-%d %H:%M:%S"))
allowedErrorNumber = 20
stat = ""
cmd_getinfo = "bitcoin-cli getinfo"
cmd_backuplog = "sudo cp -f /home/pi/DV3/Coin/debug.log /home/pi/DV3/Coin/debug.log.bak"
cmd_startnode = "sudo bitcoind -daemon"
cmd_reboot = "sudo reboot"


def run(cmd):
    return(check_output("%s" % cmd, shell=True).decode("UTF-8"))


def get_info():
    try:
        return(run(cmd_getinfo))
    except:
        return ("error")


def push_to_phone(txt):
    txt = str(txt)
    os.system('/usr/bin/pushbullet.sh "%s" &> /dev/null' % txt)


def getErrorNumber():
    errorfile = open("/tmp/bitcoin_error.txt", "r")
    errornumber = errorfile.readline(1)
    errorfile.close()
    return int(errornumber)


def increaseErrorNumber(n):
    errornumber = getErrorNumber()
    errornumber += n
    errorfile = open("/tmp/bitcoin_error.txt", "w")
    errorfile.write(str(errornumber))
    errorfile.close()


def zeroErrorNumber():
    errorfile = open("/tmp/bitcoin_error.txt", "w")
    errorfile.write("0")
    errorfile.close()


def checkstat():
    # get height of the latest block from btc.com
    apiReadout = urllib2.urlopen(
        'https://chain.api.btc.com/v3/block/latest').read()
    blockNumber = int(apiReadout[apiReadout.find(
        "height") + 8:apiReadout.find("height") + 14])
    # get height of the latest block from bitcoin-cli
    info = str(get_info())
    print (info)
    # cases:
    if info.find("version") == -1:  # no response
        # run(cmd_backuplog)
        if getErrorNumber() > allowedErrorNumber:
            # get too many error already, reboot
            stat = "RaspberryPi restarting"
            push_to_phone(stat)
            print (stat)
            run(cmd_reboot)
        else:  # try restart bitcoind
            run(cmd_startnode)
            increaseErrorNumber(5)
            stat = "Bitcoin node restarting"
            push_to_phone(stat)
            print (stat)
    else:  # can find version information
        blockNumberCli = int(
            info[info.find("blocks") + 9:info.find("blocks") + 15])
        diff = blockNumberCli - blockNumber
        if diff > 3:  # off sync over 3 blocks, abnormal
            stat = "Bitcoin node offSync %i blocks" % diff
            push_to_phone(stat)
            print (stat)
            increaseErrorNumber(1)  # add error score
            if getErrorNumber() > allowedErrorNumber:
                # get too many error already, reboot
                stat = "RaspberryPi restarting"
                push_to_phone(stat)
                print (stat)
                run(cmd_reboot)
        else:
            stat = "Bitcoin node Running OK, offset %i block" % diff
            print (stat)
            zeroErrorNumber()  # everything is fine


# Start check:
checkstat()
