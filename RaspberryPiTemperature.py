from subprocess import check_output
from re import findall
from time import strftime
import os


def get_temp():
    temp = check_output(["vcgencmd", "measure_temp"])
    temp = temp.decode("UTF-8")
    temp = findall("\d+\.\d+", temp)
    temp = temp[0]
    temp = float(temp)
    return(temp)


def write_temp(temp):
    with open("cpu_temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(temp)))


temp = get_temp()
write_temp(temp)

if temp > 75:
    os.system('/usr/bin/pushbullet.sh "RP is %s Degree!!!"' % temp)
