from subprocess import check_output
from subprocess import CalledProcessError
import os
import urllib2
from time import strftime
# from tendo import singleton
# me = singleton.SingleInstance()

# Initialize
print (strftime("%Y-%m-%d %H:%M:%S"))
allowedErrorNumber = 20
stat = ""
cmd_getinfo = "curl 127.1:7332"
cmd_startnode = "bcoin --daemon"
cmd_reboot = "sudo reboot"


def run(cmd):
    return(check_output("%s" % cmd, shell=True).decode("UTF-8"))


def get_info():
    try:
        return(run(cmd_getinfo))
    except CalledProcessError as e:
        error = e.output
        if error.find("code") == -1:
            error = "error"
        return (error)


def push_to_phone(txt):
    txt = str(txt)
    os.system('/usr/bin/pushbullet.sh "%s" &> /dev/null' % txt)


def getErrorNumber():
    errorfile = open("/home/pi/bcoin_error.txt", "r")
    errornumber = errorfile.readline(1)
    errorfile.close()
    return int(errornumber)


def increaseErrorNumber(n):
    errornumber = getErrorNumber()
    errornumber += n
    errorfile = open("/home/pi/bcoin_error.txt", "w")
    errorfile.write(str(errornumber))
    errorfile.close()


def zeroErrorNumber():
    errorfile = open("/home/pi/bcoin_error.txt", "w")
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
    if info == "error":  # no response
        if getErrorNumber() > allowedErrorNumber:
            # get too many error already, reboot
            stat = "RaspberryPi restarting"
            push_to_phone(stat)
            print (stat)
            run(cmd_reboot)
        else:  # try restart bcoind
            run(cmd_startnode)
            increaseErrorNumber(5)
            stat = "Bcoin node restarting"
            push_to_phone(stat)
            print (stat)
    if info.find("version") != -1:  # can find version information
        blockNumberCli = int(
            info[info.find("height") + 9:info.find("height") + 15])
        diff = blockNumber - blockNumberCli
        if diff > 6:  # off sync over 6 blocks, abnormal
            stat = "Bcoin node offSync %d blocks" % diff
            push_to_phone(stat)
            print (stat)
            # increaseErrorNumber(1)  # add error score
            if getErrorNumber() > allowedErrorNumber:
                # get too many error already, reboot
                stat = "RaspberryPi restarting"
                push_to_phone(stat)
                print (stat)
                run(cmd_reboot)
        else:
            stat = "Bcoin node Running OK, offset %d block" % diff
            print (stat)
            zeroErrorNumber()  # everything is fine


# Start check:
checkstat()
