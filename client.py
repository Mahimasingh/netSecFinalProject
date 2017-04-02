# chat_client.py
#python client.py -u Alice -sip 127.0.0.1 -sp 3000

import sys
import socket
import select
import argparse
import json

PEER_LIST = {}
SOCKET_LIST =[]
RECV_BUFFER = 4096

def arguments(arglist):
    parser = argparse.ArgumentParser(description='Simple chat server')
    parser.add_argument('-u', required=True, dest='user', help="User to be logged into server")
    #parser.add_argument('-p', required=True, dest='userPass', help="User password for server authentication")
    parser.add_argument('-sip', required=True, dest='server', help="IP address of the server")
    parser.add_argument('-sp', required=True, dest='port', type=int, help="port to connect to server")
    return parser.parse_args(arglist)



def server_authentication(args):

    user = args.user
    server = args.server
    port = args.port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote server
    try :
        s.connect((server, port))
    except :
        print 'Unable to connect'
        sys.exit()



    s.send(user)
    SOCKET_LIST.append(s)
    print 'Connected to remote server. You can start sending messages'


def connect_to_peer(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote server
    try :
        s.connect((addr[0], addr[1]))
    except :
        print 'Unable to connect'
        sys.exit()

    SOCKET_LIST.append(s)



def chat_client():
    PEER_LIST = {}
    sys.stdout.write('[ME] >'); sys.stdout.flush()
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        #print SOCKET_LIST


        for sock in ready_to_read:
            print PEER_LIST
        # process data recieved from client,
            try:
                # receiving data from the socket.
                data = sock.recv(RECV_BUFFER)
                if data:
                    sys.stdout.write("\n")
                    # this may need to change
                    pack = json.loads(data)
                    for key in pack:
                        if key == 'peer':
                            PEER_LIST = pack[key]
                    sys.stdout.write(data)
                    sys.stdout.flush()
                    sys.stdout.write('\n[ME] >'); sys.stdout.flush()
                else:
                    # remove the socket that's broken
                    print "we killed the socket"
                    if sock in SOCKET_LIST:
                        SOCKET_LIST.remove(sock)

                        # exception
            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)          # __str__ allows args to be printed directly,
                                     # but may be overridden in exception subclasses


            msg = sys.stdin.readline()
            if str(msg) == "list\n":
                #received list command
                                print("received list command")
                                print PEER_LIST
                                for peer in PEER_LIST:
                                    print(peer)
                                sys.stdout.write('[ME] >'); sys.stdout.flush()
            elif str(msg[:4]) == "send":
                                print("get send")
                                sending = data.split()
                                for name in PEER_LIST:
                                    if sending[1] == name:
                                        print("received send command")
                                        SOCKET_LIST[PEER_LIST.index(name)+1].send("\r" + '[FROM' + str(sock.getpeername()) + name + '] ' + " ".join(sending[2:])+"\n")
                                        sys.stdout.write('[ME] >'); sys.stdout.flush()

            else:
                #print("Unrecognized command")
                sys.stdout.write('[ME] >'); sys.stdout.flush()







    server_socket.close()

if __name__ == "__main__":
    #user1$ python ChatClient.py -u Alice -sip server-ip -sp 9090

    args = arguments(sys.argv[1:])
    server_authentication(args)
    sys.exit(chat_client())
