upgrade = False

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
            '/usr/bin/pushbullet.sh "New version of dev installed" &> /dev/null', shell=True).decode("UTF-8"))
    except CalledProcessError as e:
        print(e.output)
    # try:
    #    print (check_output("sudo reboot", shell=True).decode("UTF-8"))
    # except CalledProcessError as e:
    #    print(e.output)

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
