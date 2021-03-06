from subprocess import check_output
# from subprocess import CalledProcessError
import os
import urllib.request
from time import strftime

# Initialize
print (strftime("%Y-%m-%d %H:%M:%S"))
allowedErrorNumber = 20
stat = ""
cmd_getinfo = "bitcoin-cli getinfo"
cmd_startnode = "bitcoind"
cmd_reboot = "sudo reboot"


def run(cmd):
    return(check_output("%s" % cmd, shell=True).decode("UTF-8"))


def get_info():
    try:
        return(run(cmd_getinfo))
    except ValueError:
        return ("error")


def push_to_phone(txt):
    txt = str(txt)
    os.system('/usr/bin/pushbullet.sh "%s" &> /dev/null' % txt)


def getErrorNumber():
    errorfile = open("/home/pi/bitcoin_error.txt", "r")
    errornumber = errorfile.readline(1)
    errorfile.close()
    return int(errornumber)


def increaseErrorNumber(n):
    errornumber = getErrorNumber()
    errornumber += n
    errorfile = open("/home/pi/bitcoin_error.txt", "w")
    errorfile.write(str(errornumber))
    errorfile.close()


def zeroErrorNumber():
    errorfile = open("/home/pi/bitcoin_error.txt", "w")
    errorfile.write("0")
    errorfile.close()


def checkstat():
    # get height of the latest block from btc.com
    apiReadout = str(urllib.request.urlopen(
        'https://chain.api.btc.com/v3/block/latest').read())
    blockNumber = int(apiReadout[apiReadout.find(
        "height") + 8:apiReadout.find("height") + 14])
    # get height of the latest block from bitcoin-cli
    info = str(get_info())
    print (info)
    # cases:
    if getErrorNumber() > allowedErrorNumber:
            # get too many error already, reboot
        stat = "RaspberryPi restarting"
        push_to_phone(stat)
        print (stat)
        run(cmd_reboot)
    if info == "error":  # no response
        increaseErrorNumber(2)  # add error score
        run(cmd_startnode)
        stat = "Bitcoin node restarting"
        push_to_phone(stat)
        print (stat)
    if info.find("version") != -1:  # can find version information
        blockNumberCli = int(
            info[info.find("blocks") + 9:info.find("blocks") + 15])
        diff = blockNumber - blockNumberCli
        if diff > 6:  # off sync over 6 blocks, abnormal
            stat = "Bitcoin node Running, offSync %d blocks" % diff
            push_to_phone(stat)
            print (stat)
            increaseErrorNumber(1)  # add error score
        else:
            stat = "Bitcoin node Running OK, offset %d block" % diff
            print (stat)
            zeroErrorNumber()  # everything is fine


# Start check:
checkstat()
