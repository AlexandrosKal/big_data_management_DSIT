#!/usr/bin/env python3
import argparse
import random
import socket
from my_utils import *


def connect_to_servers(srv_address_port):
    # attempt to connect to the servers in srv_address_port
    # remove the servers that are unreachable from the list
    servers_down = []
    socket_list = []
    for (add, port) in srv_address_port:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((add, port))
            socket_list.append(s)
        except socket.error as e:
            print(f'Could not connect to {add}:{port}, Error: {e}')
            servers_down.append((add, port))
    for (add, port) in servers_down:
        srv_address_port.remove((add, port))
    return socket_list


def close_sockets(socket_list):
    # close the sockets when no longer needed
    for s in socket_list:
        try:
            s.close()
        except socket.error as e:
            print(f'Could not close socket {s}')
            print(f'Error: {e}')
    return


def read_data(filename):
    # read the the data to index from the specified file
    data_to_send = []
    f = open(filename, "r")
    for ln in f.readlines():
        ln = ln.rstrip()
        data_to_send.append(ln)
    f.close()
    return data_to_send


def parse_server_file(filename):
    # parse the file with the server addresses and ports
    address_port_pairs = []
    f = open(filename, "r")
    for ln in f.readlines():
        ln = ln.rstrip()
        add, port = ln.split()
        address_port_pairs.append((add, int(port)))
    f.close()
    return address_port_pairs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default='serverFile.txt', help='Server file location')
    parser.add_argument('-i', type=str, default='dataToIndex.txt', help='Location of data to be indexed')
    parser.add_argument('-k', type=int, default=2, help='replication factor')
    ARGS = parser.parse_args()

    print("Broker Started")
    data_to_send = read_data(ARGS.i)
    srv_address_port = parse_server_file(ARGS.s)
    buf_size = 2048
    socket_list = connect_to_servers(srv_address_port)
    initial_no_of_srv = len(socket_list)
    top_lvl_keys = []

    # Send the data to be indexed to random (ARGS.k) servers
    for line in data_to_send:
        random.shuffle(socket_list)
        if len(socket_list) < ARGS.k:
            print('Not enough servers available...')
            exit()
        top_lvl_key, _ = line.split(' ', 1)
        top_lvl_key = top_lvl_key.strip()
        response = ''
        if top_lvl_key in top_lvl_keys:
            print('Warning: Top level keys must be unique...Skipping line')
            continue
        for s in socket_list[0:ARGS.k]:
            top_lvl_keys.append(top_lvl_key)
            msg = 'PUT ' + line
            msg = msg.encode('UTF-8')
            try:
                send_full_msg(s, msg)
                data = receive_msg(s)
                response = data.decode('UTF-*')
            except socket.error as e:
                print(f'Error: {e}')
            print(response)
    close_sockets(socket_list)

    # Start waiting for user commands
    while True:
        usr_in = input('kv_broker->: ')
        # try to connect to the servers in the srv_address_port list
        socket_list = connect_to_servers(srv_address_port)
        active_servers = len(socket_list)
        dc_servers = initial_no_of_srv - active_servers
        if len(socket_list) == 0:
            print('No connected server. Exiting...')
            exit()
        msg = usr_in.encode('UTF-8')
        tokens = usr_in.split(' ', 1)
        cmd_name = tokens[0]
        if len(tokens) > 1:
            cmd_body = tokens[1]
        if cmd_name == 'exit':
            break
        elif cmd_name == 'GET':
            if dc_servers >= ARGS.k:
                print('Warning: K or more servers are down GET might be unreliable')
            response = ''
            for s in socket_list:
                try:
                    send_full_msg(s, msg)
                    data = receive_msg(s)
                    response = data.decode('UTF-8')
                    if data is not None and data != b"NOT FOUND":
                        break
                except socket.error as e:
                    print(f'Error: {e}')
            print(response)
        elif cmd_name == 'QUERY':
            if dc_servers >= ARGS.k:
                print('Warning: K or more servers are down QUERY might be unreliable')
            response = ''
            for s in socket_list:
                try:
                    send_full_msg(s, msg)
                    data = receive_msg(s)
                    response = data.decode('UTF-8')
                    if data is not None and data != b"NOT FOUND":
                        break
                except socket.error as e:
                    print(f'Error: {e}')
            print(response)
        elif cmd_name == 'DELETE':
            if dc_servers > 0:
                print('Warning: One or more servers are down DELETE operation is unavailable')
                close_sockets(socket_list)
                socket_list = []
                continue
            response = ''
            not_found = True
            count_ok_deletions = 0
            for s in socket_list:
                try:
                    send_full_msg(s, msg)
                    data = receive_msg(s)
                    response = data.decode('UTF-8')
                    if data is not None and data != b"NOT FOUND":
                        if data != b"DELETE OK":
                            break
                        if not_found:
                            not_found = False
                        count_ok_deletions += 1
                        if count_ok_deletions == ARGS.k:
                            break
                except socket.error as e:
                    print(f'Error: {e}')
            if not_found:
                print(response)
            elif count_ok_deletions == ARGS.k:
                print(response)
            elif count_ok_deletions:
                print('ERROR: delete not performed in K servers')
        else:
            print('ERROR: Unknown command')
        close_sockets(socket_list)
        socket_list = []
    close_sockets(socket_list)

