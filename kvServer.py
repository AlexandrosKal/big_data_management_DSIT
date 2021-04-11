#!/usr/bin/env python3
import argparse
import socket
import trie as tr
from my_utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, default='127.0.0.1', help='Server address')
    parser.add_argument('-p', type=int, default='65432', help='Server port')
    ARGS = parser.parse_args()

    HOST = ARGS.a
    PORT = ARGS.p
    print("Server started.")
    buf_size = 2048
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print('Connected: ', addr)
    my_trie = tr.TrieNode()
    while True:
        try:
            data = receive_msg(conn)
            if not data:
                conn, addr = s.accept()
                continue
            msg = data.decode('UTF-8')
            tokens = msg.split(' ', 1)
        except socket.error as e:
            print(f'Error: {e}')

        if len(tokens) < 2:
            response = 'ERROR: Syntax error in request'
            send_full_msg(conn, response.encode('UTF-8'))
            continue
        cmd_name = tokens[0]
        cmd_body = tokens[1]

        if cmd_name == 'PUT':
            if check_syntax(cmd_body) is False:
                response = 'ERROR: Syntax error in request body'
                try:
                    send_full_msg(conn, response.encode('UTF-8'))
                except socket.error as e:
                    print(f'Error: {e}')
            else:
                top_lvl_key, values = cmd_body.split(':', 1)
                top_lvl_key = top_lvl_key.strip()
                values = values.strip()
                json_body = body_to_json(values)
                values_dict = json.loads(json_body)
                if my_trie.put(top_lvl_key, values_dict):
                    response = 'OK'
                else:
                    response = 'ERROR: could not perform put'
                try:
                    send_full_msg(conn, response.encode('UTF-8'))
                except socket.error as e:
                    print(f'Error: {e}')

        elif cmd_name == 'GET':
            top_lvl_key = cmd_body.strip()
            value = my_trie.get(top_lvl_key)
            if value is None:
                response = 'NOT FOUND'
            else:
                response = top_lvl_key + ' : ' + json_to_body(json.dumps(value))
            try:
                send_full_msg(conn, response.encode('UTF-8'))
            except socket.error as e:
                print(f'Error: {e}')
        elif cmd_name == 'QUERY':
            q_tokens = cmd_body.split(".")
            resp_start = cmd_body.strip()
            for i, qt in enumerate(q_tokens):
                if i > 0:
                    q_tokens[i] = qt.strip().strip('\""')
                else:
                    q_tokens[i] = qt.strip()
            value = my_trie.query(q_tokens[0], q_tokens[1:])
            if value is None:
                response = 'NOT FOUND'
            else:
                response = resp_start + ' : ' + json_to_body(json.dumps(value))
            try:
                send_full_msg(conn, response.encode('UTF-8'))
            except socket.error as e:
                print(f'Error: {e}')
        elif cmd_name == 'DELETE':
            top_lvl_key = cmd_body.strip()
            print(f'Getting: {top_lvl_key}')
            value = my_trie.delete(top_lvl_key)
            if value is None:
                response = 'NOT FOUND'
            else:
                response = "DELETE OK"
            try:
                send_full_msg(conn, response.encode('UTF-8'))
            except socket.error as e:
                print(f'Error: {e}')
        else:
            response = 'ERROR: Unknown command'
            print(response)
            try:
                send_full_msg(conn, response.encode('UTF-8'))
            except socket.error as e:
                print(f'Error: {e}')
    conn.close()
    s.close()
