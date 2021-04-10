import json
import struct


def check_syntax(line):
    # transform line to json since it is a pretty similar format
    # and test if it is syntactically correct
    json_line = '{ ' + line.replace(';', ',') + ' }'
    try:
        _ = json.loads(json_line)
    except ValueError as e:
        print('Syntax error')
        print(json_line)
        return False
    return True


def json_to_my_form(line):
    line = line.replace('{', '{ ')
    line = line.replace('}', ' }')
    line = line.replace('{  }', '{}')
    line = line.strip('{')
    line = line.strip('}')
    line = line.strip()
    line = line.replace(',', ' ;')
    line = line.replace(':', ' :')
    return line


def body_to_json(line):
    # transform the body of a put request to json for easier handling
    json_line = line.replace(';', ',')
    return json_line


def json_to_body(line):
    # transform a json line to the format requested in the assignment
    line = line.replace('{', '{ ')
    line = line.replace('}', ' }')
    line = line.replace('{  }', '{}')
    line = line.replace(',', ' ;')
    line = line.replace(':', ' :')
    return line


def send_full_msg(s, msg):
    # append an unsigned int before each message
    # that signifies the message length
    msg_size = len(msg)
    to_send = struct.pack('>I', msg_size) + msg
    s.sendall(to_send)
    return


def receive_msg(s):
    bin_msg_len = recv_all(s, 4)
    if not bin_msg_len:
        return None
    msg_len = struct.unpack('>I', bin_msg_len)[0]
    full_message = recv_all(s, msg_len)
    return full_message


def recv_all(s, msg_size):
    # utilizing the prefix of each message that denotes its length
    # keep reading until the full message is read
    chunks = []
    len_so_far = 0
    while len_so_far < msg_size:
        chunk = s.recv(msg_size, len_so_far)
        if not chunk:
            break
        len_so_far += len(chunk)
        chunks.append(chunk)
    return b"".join(chunks)


