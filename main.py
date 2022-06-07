import os
import re
import keyboard
from time import sleep
from datetime import date
from sys import exit

# EASY REGIST dan REGIST ULANG

layanan = {'2801': '10', '2802': '10', '2828': '20', '2887': '5', '2888': '20', '2889': '50', '2890': '100',
           '1601': '10', '1602': '20', '1603': '30', '1604': '50', '1605': '100', '2820': '10', '2830': '20',
           '2819': '50', '2900': '', '2901': '', '2902': '', '2903': '', '2904': '', '2905': '', '2906': '',
           '2907': '', '2908': '', '2909': '', '2910': '', '2911': '', '2912': '', '2913': '', '2914': '',
           '2915': '', '2916': '', '2917': '', '2918': '', '2919': '', '2920': '', '2921': ''}


def clear():
    os.system('cls')


def input_sn():
    while True:
        sn = input('Masukkan SN pelanggan: ')
        if len(sn) == 12 or len(sn) == 16:
            break
        else:
            print('\nTolong masukkan sn yang benar')
    clear()
    return sn


def input_fsp(brand='rcm'):
    pattern = {'zte': r'\d/\d/\d+/\d+', 'rcm': r'\d/\d+/\d+', 'bdc': r'\d+/\d+'}
    while True:
        if brand == 'bdc':
            print("Masukkan FSP dengan format 'P/Onu id'")
            fsp = input('P/O: ')
        elif brand == 'rcm':
            print("Masukkan FSP dengan format 'S/P/Onu id'")
            fsp = input('S/P/O: ')
        else:
            print("Masukkan FSP dengan format 'F/S/P/Onu id'")
            fsp = input('F/S/P/O: ')
        if re.match(pattern[brand], fsp) is not None:
            break
        elif fsp.lower() == 'h':
            regist()
        else:
            clear()
            print('\nTolong input FSP dengan format yang benar\n')
    clear()
    return fsp


def input_vlan():
    while True:
        vlan = input('Masukkan VLAN: ')
        if vlan in layanan.keys():
            break
        elif vlan.lower() == 'h':
            regist()
        else:
            clear()
            print('\nTolong input vlan dengan benar')
    clear()
    return vlan


def input_lineprofile():
    while True:
        lineprofile = input('Masukkan nomor lineprofile: ')
        if lineprofile.lower() == 'h':
            regist()
        elif lineprofile.isdigit():
            lineprofile = int(lineprofile)
            if 0 < lineprofile < 30:
                break
        else:
            clear()
            print('Masukkan nomor lineprofile dengan benar')
    clear()
    return lineprofile


def input_serviceport():
    while True:
        serviceport = input('Masukkan nomor serviceport: ')
        if serviceport.lower() == 'h':
            regist()
        elif serviceport.isdigit():
            serviceport = int(serviceport)
            break
        else:
            clear()
            print('Masukkan nomor serviceport dengan benar')
    clear()
    return serviceport


def input_description():
    while True:
        print('Tolong masukkan description')
        sid = input('Masukkan SID pelanggan: ')
        if sid.isdigit():
            break
        elif sid.lower() == 'h':
            regist()
        else:
            clear()
            print('Tolong input SID dengan benar\n')
            continue
    clear()
    print('Tolong masukkan description')
    print('Masukkan SID pelanggan: ' + sid)
    user = input('Masukkan nama pelanggan: ')
    if user.lower() == 'h':
        regist()
    split_user = user.split()
    if len(split_user) > 1:
        nama = ''
        for i in split_user:
            nama += i
            nama += '.'
        nama = nama[:-1]
    else:
        nama = user.replace(' ', '')
    clear()
    return sid, nama


def input_pppoe():
    print('Apakah password PPPoE merupakan tanggal hari ini?')
    while True:
        pw_hari_ini = input('Y/N: ')
        if pw_hari_ini[0].lower() in ['y', 'n']:
            break
        elif pw_hari_ini.lower() == 'h':
            regist()
        else:
            clear()
            print('\nTolong input dengan benar')
    clear()
    if pw_hari_ini == 'n':
        while True:
            password = input('Masukkan password:  ')
    else:
        today = str(date.today())
    password = today.replace('-', '')
    clear()
    return password


def retry():
    while True:
        print('\n\nApakah anda ingin regist lagi?')
        retry = input('Y/N: ')
        if retry[0].lower() in ['y', 'n']:
            return retry
        else:
            clear()
            print('Tolong input dengan benar')


def input_nce():
    while True:
        print('Menggunakan NCE?')
        nce = input('Y/N:  ')
        if nce[0].lower() in ['y', 'n']:
            break
        elif nce.lower() == 'h':
            regist()
        else:
            clear()
            print('Tolong input dengan benar')


def raisecom(baru_or_ulang, pppoe_or_ipoe):
    sn = input_sn()
    fsp = input_fsp('rcm')
    split_fsp = re.split(r'\D', fsp)
    vlan = input_vlan()
    lineprofile = input_lineprofile()
    sid, nama = input_description()

    if baru_or_ulang == '2':
        rcm_first_part = (f'\n'
                          f'config\n'
                          f'interface gpon-olt {split_fsp[0]}/{split_fsp[1]}\n'
                          f'no create gpon-onu {split_fsp[2]}\n'
                          f'create gpon-onu {split_fsp[2]} sn {sn} line-profile-id {lineprofile} service-profile-id 1\n'
                          f'quit\n'
                          f'interface gpon-onu {fsp}\n'
                          f'description {sid}-{nama} \n'
                          f'quit\n')
    else:
        rcm_first_part = (f'config\n'
                          f'interface gpon-olt {split_fsp[0]}/{split_fsp[1]}\n'
                          f'create gpon-onu {split_fsp[2]} sn {sn} line-profile-id {lineprofile} service-profile-id 1\n'
                          f'quit\n'
                          f'interface gpon-onu {fsp}\n'
                          f'description {sid}-{nama} \n'
                          f'quit')

    if sn[:3].lower() == 'rcm':
        if pppoe_or_ipoe == '1':
            password = input_pppoe()
            clear()
            rcm_second_part = (f"gpon-onu {fsp}\n"
                               f"iphost 1 mode pppoe\n"
                               f"iphost 1 pppoe username {sn} password {password}\n"
                               f"iphost 1 vlan {vlan}\n"
                               f"iphost 1 service Internet\n"
                               f"iphost 1 service mode route nat enable cos 0 portlist 1,2 ssidlist 1\n"
                               f"end")
        else:
            rcm_second_part = (f"gpon-onu {fsp}\n"
                               f"iphost 1 mode dhcp\n"
                               f"iphost 1 vlan {vlan}\n"
                               f"iphost 1 service Internet\n"
                               f"iphost 1 service mode route nat enable cos 0 portlist 1,2 ssidlist 1\n"
                               f"end")

        rcm_all_part = rcm_first_part + '\n' + rcm_second_part
    else:
        rcm_all_part = rcm_first_part

    def print_rcm():
        if sn[:3].lower() == 'rcm':
            keyboard.write(rcm_first_part, delay=0.01)
            keyboard.release('ctrl')
            keyboard.release('alt')
            keyboard.send('enter')
            sleep(4)
            keyboard.release('ctrl')
            keyboard.release('alt')
            keyboard.write(rcm_second_part, delay=0.01)
            keyboard.release('ctrl')
            keyboard.release('alt')
            keyboard.wait('Esc')
        else:
            keyboard.write(rcm_first_part, delay=0.01)
            keyboard.release('ctrl')
            keyboard.release('alt')
            keyboard.send('enter')
            keyboard.wait('Esc')

    print(rcm_all_part)
    keyboard.add_hotkey('alt+space+ctrl', print_rcm)


def c610(baru_or_ulang, pppoe_or_ipoe):
    global password
    sn = input_sn()
    fsp = input_fsp('zte')
    split_fsp = re.split('\D', fsp)
    vlan = input_vlan()
    sid, nama = input_description()

    if baru_or_ulang == '2':
        c610_first_part = (f'config t\n'
                           f'interface gpon_olt-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}\n'
                           f'no onu {split_fsp[3]}\n'
                           f'onu {split_fsp[3]} type ZTEG-F609 sn {sn}\n'
                           f'exit\n')
    else:
        c610_first_part = (f'config t\n'
                           f'interface gpon_olt-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}\n'
                           f'onu {split_fsp[3]} type ZTEG-F609 sn {sn}\n'
                           f'exit\n'
                           f'        ')

    if pppoe_or_ipoe == '1':
        password = input_pppoe()
        clear()
        c610_second_part = (f'interface gpon_onu-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                            f'description {sid}-{nama}\n'
                            f'tcont 1 name HSI profile PPPOE\n'
                            f'gemport 1 name HSI tcont 1\n'
                            f'exit\n'
                            f'interface vport-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}.{split_fsp[3]}:1\n'
                            f'service-port 1 user-vlan {vlan} vlan {vlan}\n'
                            f'exit')
    else:
        c610_second_part = (f'interface gpon_onu-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                            f'description {sid}-{nama}\n'
                            f'tcont 1 name HSI profile {layanan[vlan]}Mbps\n'
                            f'gemport 1 name HSI tcont 1\n'
                            f'exit\n'
                            f'interface vport-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}.{split_fsp[3]}:1\n'
                            f'service-port 1 user-vlan {vlan} vlan {vlan}\n'
                            f'exit')
    if sn[:3].lower() == 'zte':
        if pppoe_or_ipoe == '2':
            c610_third_part = (f'pon-onu-mng gpon_onu-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                               f'service HSI gemport 1 vlan {vlan}\n'
                               f'wan-ip ipv4 mode dhcp vlan-profile vlan{vlan} host 1\n'
                               f'vlan port eth_0/1 mode tag vlan {vlan}\n'
                               f'vlan port eth_0/2 mode tag vlan {vlan}\n'
                               f'dhcp-ip ethuni eth_0/1 from-onu\n'
                               f'dhcp-ip ethuni eth_0/2 from-onu\n'
                               f'end')
        else:
            c610_third_part = (f'pon-onu-mng gpon_onu-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                               f'service HSI gemport 1 vlan {vlan}\n'
                               f'wan-ip ipv4 mode pppoe username {sn} password {password} vlan-profile vlan{vlan} host 1\n '
                               f'wan-ip ipv4 mode pppoe username {sn} password {password} vlan-profile wan{vlan} host 1\n '
                               f'vlan port eth_0/1 mode tag vlan {vlan}\n'
                               f'vlan port eth_0/2 mode tag vlan {vlan}\n'
                               f'dhcp-ip ethuni eth_0/1 from-onu\n'
                               f'dhcp-ip ethuni eth_0/2 from-onu\n'
                               f'end')
    else:
        c610_third_part = (f'pon-onu-mng gpon_onu-{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                           f'service HSI gemport 1 vlan {vlan}\n'
                           f'vlan port eth_0/1 mode tag vlan {vlan}\n'
                           f'vlan port eth_0/2 mode tag vlan {vlan}\n'
                           f'dhcp-ip ethuni eth_0/1 from-onu\n'
                           f'dhcp-ip ethuni eth_0/2 from-onu\n'
                           f'end')
    c610_all_part = c610_first_part + '\n' + c610_second_part + '\n' + c610_third_part

    def print_c610():
        keyboard.write(c610_first_part, delay=0.01)
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.send('enter')
        keyboard.write(c610_second_part, delay=0.01)
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.send('enter')
        keyboard.write(c610_third_part, delay=0.01)
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.send('enter')
        keyboard.wait('Esc')

    print(c610_all_part)
    keyboard.add_hotkey('alt+space+ctrl', print_c610)


def c320(baru_or_ulang, pppoe_or_ipoe):
    global password
    sn = input_sn()
    fsp = input_fsp('zte')
    split_fsp = re.split('\D', fsp)
    vlan = input_vlan()
    sid, nama = input_description()

    if baru_or_ulang == '2':
        c320_first_part = (f'config t\n'
                           f'interface gpon-olt_{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}\n'
                           f'no onu {split_fsp[3]}\n'
                           f'onu {split_fsp[3]} type ZTEG-F609 sn {sn}\n'
                           f'exit')
    else:
        c320_first_part = (f'config t\n'
                           f'interface gpon-olt_{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}\n'
                           f'onu {split_fsp[3]} type ZTEG-F609 sn {sn}\n'
                           f'exit')

    if pppoe_or_ipoe == '1':
        password = input_pppoe()
        clear()
        c320_second_part = (f'interface gpon-onu_{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                            f'description {sid}-{nama}\n'
                            f'sn-bind enable sn\n'
                            f'tcont 1 name HSI profile PPPOE\n'
                            f'gemport 1 name HSI tcont 1\n'
                            f'service-port 1 vport 1 user-vlan {vlan} vlan {vlan}\n'
                            f'exit')
    else:
        c320_second_part = (f'interface gpon-onu_{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                            f'description {sid}-{nama}\n'
                            f'sn-bind enable sn\n'
                            f'tcont 1 name HSI profile {layanan[vlan]}Mbps\n'
                            f'gemport 1 name HSI tcont 1\n'
                            f'service-port 1 vport 1 user-vlan {vlan} vlan {vlan}\n'
                            f'exit')
    if sn[:3].lower() == 'zte':
        if pppoe_or_ipoe == '1':
            c320_third_part = (f'pon-onu-mng gpon-onu_{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                               f'service HSI gemport 1 vlan {vlan}\n'
                               f'wan-ip 1 mode pppoe username {sn} password {password} vlan-profile vlan{vlan} host 1\n'
                               f'vlan port eth_0/1 mode tag vlan {vlan}\n'
                               f'dhcp-ip ethuni eth_0/1 from-onu\n'
                               f'end')
        else:
            c320_third_part = (f'pon-onu-mng gpon-onu_{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                               f'service HSI gemport 1 vlan {vlan}\n'
                               f'wan-ip 1 mode dhcp vlan-profile vlan{vlan} host 1\n'
                               f'wan-ip 1 mode dhcp vlan-profile wan{vlan} host 1\n'
                               f'vlan port eth_0/1 mode tag vlan {vlan}\n'
                               f'dhcp-ip ethuni eth_0/1 from-onu\n'
                               f'end')
    else:
        c320_third_part = (f'pon-onu-mng gpon-onu_{split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]}:{split_fsp[3]}\n'
                           f'service HSI gemport 1 vlan {vlan}\n'
                           f'vlan port eth_0/1 mode tag vlan {vlan}\n'
                           f'dhcp-ip ethuni eth_0/1 from-onu\n'
                           f'end')

    c320_all_part = c320_first_part + '\n' + c320_second_part + '\n' + c320_third_part

    def print_c320():
        keyboard.write(c320_first_part, delay=0.01)
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.send('enter')
        keyboard.write(c320_second_part, delay=0.01)
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.send('enter')
        keyboard.write(c320_third_part, delay=0.01)
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.send('enter')
        keyboard.wait('Esc')

    print(c320_all_part)
    keyboard.add_hotkey('alt+space+ctrl', print_c320)


def bdcom(pppoe_or_ipoe):
    sn = input_sn()
    fsp = input_fsp('bdc')
    split_fsp = re.split('\D', fsp)
    vlan = input_vlan()
    sid, nama = input_description()

    if pppoe_or_ipoe == '1':
        password = input_pppoe()
        if sn[:4].lower() == '5a54':
            bdcom_all_part = (f'config\n'
                              f'interface gpoN 0/{split_fsp[0]}:{split_fsp[1]}\n'
                              f'description {sid}-{nama}\n'
                              f'gpon onu flow-mapping-profile ZTE\n'
                              f'gpon onu wan 1 admin-status enable\n'
                              f'gpon onu wan 1 nat enable\n'
                              f'gpon onu wan 1 service-type internet\n'
                              f'gpon onu wan 1 connection-type pppoe\n'
                              f'gpon onu wan 1 pppoe username {sn} password {password}\n'
                              f'gpon onu wan 1 tci vlan {vlan}\n'
                              f'gpon onu wan 1 bind lan1 lan2 ssid1\n'
                              f'gpon onu wan 1 auto-get-dns-address enable\n'
                              f'gpon onu wan 1 lan-dhcp enable\n'
                              f'quit\n'
                              f'write all')
        else:
            bdcom_all_part = (f'config\n'
                              f'interface gpoN 0/{split_fsp[0]}:{split_fsp[1]}\n'
                              f'description {sid}-{nama}\n'
                              f'gpon onu wan 1 admin-status enable\n'
                              f'gpon onu wan 1 nat enable\n'
                              f'gpon onu wan 1 service-type internet\n'
                              f'gpon onu wan 1 connection-type pppoe\n'
                              f'gpon onu wan 1 pppoe username {sn} password {password}\n'
                              f'gpon onu wan 1 tci vlan {vlan}\n'
                              f'gpon onu wan 1 bind lan1 lan2 ssid1\n'
                              f'gpon onu wan 1 auto-get-dns-address enable\n'
                              f'gpon onu wan 1 lan-dhcp enable\n'
                              f'quit\n'
                              f'write all')

    else:
        if sn[:4].lower() == '5a54':
            bdcom_all_part = (f'config\n'
                              f'interface gpoN 0/{split_fsp[0]}:{split_fsp[1]}\n'
                              f'description {sid}-{nama}\n'
                              f'gpon onu flow-mapping-profile ZTE\n'
                              f'gpon onu wan 1 admin-status enable\n'
                              f'gpon onu wan 1 nat enable\n'
                              f'gpon onu wan 1 service-type internet\n'
                              f'gpon onu wan 1 connection-type pppoe\n'
                              f'gpon onu wan 1 tci vlan {vlan}\n'
                              f'gpon onu wan 1 bind lan1 lan2 ssid1\n'
                              f'gpon onu wan 1 auto-get-dns-address enable\n'
                              f'gpon onu wan 1 lan-dhcp enable\n'
                              f'quit\n'
                              f'write all')
        else:
            bdcom_all_part = (f'config\n'
                              f'interface gpoN 0/{split_fsp[0]}:{split_fsp[1]}\n'
                              f'description {sid}-{nama}\n'
                              f'gpon onu wan 1 admin-status enable\n'
                              f'gpon onu wan 1 nat enable\n'
                              f'gpon onu wan 1 service-type internet\n'
                              f'gpon onu wan 1 connection-type pppoe\n'
                              f'gpon onu wan 1 tci vlan {vlan}\n'
                              f'gpon onu wan 1 bind lan1 lan2 ssid1\n'
                              f'gpon onu wan 1 auto-get-dns-address enable\n'
                              f'gpon onu wan 1 lan-dhcp enable\n'
                              f'quit\n'
                              f'write all')

    def print_bdcom():
        keyboard.write(bdcom_all_part, delay=0.01)
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.send('enter')
        keyboard.wait('Esc')

    print(bdcom_all_part)
    keyboard.add_hotkey('alt+space+ctrl', print_bdcom)


def huawei(baru_or_ulang, pppoe_or_ipoe):
    sn = input_sn()
    fsp = input_fsp('zte')
    split_fsp = re.split('\D', fsp)
    vlan = input_vlan()
    serviceport = input_serviceport()
    sid, nama = input_description()

    if baru_or_ulang == '2':
        huawei_first_part = (f'config\n'
                             f'undo service-port {serviceport}\n'
                             f'interface gpon {split_fsp[0]}/{split_fsp[1]}\n'
                             f'ont delete {split_fsp[2]} {split_fsp[3]}\n')
    else:
        huawei_first_part = (f'config\n'
                             f'interface gpon {split_fsp[0]}/{split_fsp[1]}\n')

    if pppoe_or_ipoe == '1':
        password = input_pppoe()
        nce = input_nce()

        clear()
        if nce == 'y':
            huawei_second_part = (
                f'ont add {split_fsp[2]} {split_fsp[3]} sn-auth {sn} omci ont-lineprofile-name ICONNET.PPPOE.{vlan} ont-srvprofile-name ICONNET.PPPOE.{vlan} desc {sid}-{nama}\n\n'
                f'ont ipconfig {split_fsp[2]} {split_fsp[3]} pppoe vlan {vlan} priority 0 user-account username {sn} password {password}\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 1 enable\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 2 enable\n\n'
                f'quit\n\n'
                f'service-port vlan {vlan} gpon {split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]} ont {split_fsp[3]} gemport 1 multi-service user-vlan {vlan} tag-transform translate\n\n'
                f'quit')
        else:
            huawei_second_part = (
                f'ont add {split_fsp[2]} {split_fsp[3]} sn-auth {sn} omci ont-lineprofile-name ICONNET.PPPOE.{vlan} ont-srvprofile-name ICONNET.PPPOE.{vlan} desc {sid}-{nama}\n\n'
                f'ont ipconfig {split_fsp[2]} {split_fsp[3]} pppoe vlan {vlan} priority 0 user-account username {sn} password {password}\n\n'
                f'ont internet-config {split_fsp[2]} {split_fsp[3]} ip-index 0\n\n'
                f'ont wan-config {split_fsp[2]} {split_fsp[3]} ip-index 0 profile-name ICONNET.AUTOPROV\n\n'
                f'ont policy-route-config {split_fsp[2]} {split_fsp[3]} profile-name ICONNET.AUTOPROV\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 1 enable\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 2 enable\n\n'
                f'quit\n\n'
                f'service-port vlan {vlan} gpon {split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]} ont {split_fsp[3]} gemport 1 multi-service user-vlan {vlan} tag-transform translate\n\n'
                f'quit')
    else:
        if vlan in ['2828', '2820', '2830', '2819']:
            huawei_second_part = (
                f'ont add {split_fsp[2]} {split_fsp[3]} sn-auth {sn} omci ont-lineprofile-name AUTOPROV.{layanan[vlan]}-{vlan} ont-srvprofile-name AUTOPROV.{layanan[vlan]}-{vlan} desc {sid}-{nama}\n\n'
                f'ont ipconfig {split_fsp[2]} {split_fsp[3]} dhcp vlan {vlan} priority 0\n\n'
                f'ont internet-config {split_fsp[2]} {split_fsp[3]} ip-index 0\n\n'
                f'ont wan-config {split_fsp[2]} {split_fsp[3]} ip-index 0 profile-name ICONNET.AUTOPROV\n\n'
                f'ont policy-route-config {split_fsp[2]} {split_fsp[3]} profile-name ICONNET.AUTOPROV\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 1 enable\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 2 enable\n\n'
                f'quit\n\n'
                f'service-port vlan {vlan} gpon {split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]} ont {split_fsp[3]} gemport 1 multi-service user-vlan {vlan} tag-transform translate\n\n'
                f'quit')

        else:
            huawei_second_part = (
                f'ont add {split_fsp[2]} {split_fsp[3]} sn-auth {sn} omci ont-lineprofile-name AUTOPROV.{layanan[vlan]} ont-srvprofile-name AUTOPROV.{layanan[vlan]} desc {sid}-{nama}\n\n'
                f'ont ipconfig {split_fsp[2]} {split_fsp[3]} dhcp vlan {vlan} priority 0\n\n'
                f'ont internet-config {split_fsp[2]} {split_fsp[3]} ip-index 0\n\n'
                f'ont wan-config {split_fsp[2]} {split_fsp[3]} ip-index 0 profile-name ICONNET.AUTOPROV\n\n'
                f'ont policy-route-config {split_fsp[2]} {split_fsp[3]} profile-name ICONNET.AUTOPROV\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 1 enable\n\n'
                f'ont port route {split_fsp[2]} {split_fsp[3]} eth 2 enable\n\n'
                f'quit\n\n'
                f'service-port vlan {vlan} gpon {split_fsp[0]}/{split_fsp[1]}/{split_fsp[2]} ont {split_fsp[3]} gemport 1 multi-service user-vlan {vlan} tag-transform translate\n\n'
                f'quit')

    huawei_all_part = huawei_first_part + huawei_second_part
    print(huawei_all_part)


def regist():
    while True:
        clear()
        print('REGIST DENGAN MUDAH!!\n\n'
              'BILA INGIN KEMBALI KE MENU UTAMA TULIS HURUF "H"\n')
        while True:
            print('Registrasi baru atau registrasi (ulang/replace)')
            print('1 = Regist Baru | 2 = Regist ulang/ replace')
            baru_or_ulang = input('Masukkan angka 1/2:  ')
            if baru_or_ulang.lower() == 'h':
                regist()
            elif baru_or_ulang == '1' or baru_or_ulang == '2':
                break
            else:
                clear()
                print('Tolong input dengan benar\n')
                continue
        clear()
        while True:
            print('PPPOE atau IPOE')
            print('1 = PPPOE | 2 = IPOE')
            pppoe_or_ipoe = input('Masukkan angka 1/2:  ')
            if pppoe_or_ipoe in ['1', '2']:
                break
            elif pppoe_or_ipoe.lower() == 'h':
                regist()
            else:
                clear()
                print('Tolong input dengan benar\n')
                continue
        clear()
        while True:
            print('Tolong isi brand OLT ')
            print('1 = Raisecom | 2 = ZTE C610 | 3 = ZTE C320 | 4 = BDCOM | 5 = Huawei ')
            brand_olt = input('Masukkan angka 1-5:  ')
            if brand_olt in ['1', '2', '3', '4', '5']:
                break
            elif brand_olt.lower() == 'h':
                regist()
            else:
                clear()
                print('Tolong input dengan benar\n')
                continue
        clear()

        if brand_olt == '1':
            raisecom(baru_or_ulang, pppoe_or_ipoe)
        elif brand_olt == '2':
            c610(baru_or_ulang, pppoe_or_ipoe)
        elif brand_olt == '3':
            c320(baru_or_ulang, pppoe_or_ipoe)
        elif brand_olt == '4':
            bdcom(pppoe_or_ipoe)
        else:
            huawei(baru_or_ulang, pppoe_or_ipoe)

        again = retry()
        if again == 'y':
            continue
        else:
            exit()


if __name__ == '__main__':
    regist()
