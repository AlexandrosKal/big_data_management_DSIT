import argparse
import string
import random
from my_utils import check_syntax


def generate_key_val(lvl, key_dict, n=0):
    if lvl == ARGS.d:
        # if we are at the top level use keyN as the key
        key_str = 'key' + str(n)
    else:
        # if we are at an inner level use a random string as the key
        key_str = gen_random_string(ARGS.l)

    # set the number of keys in this entry randomly between 0 and m
    keys_in_val = random.randint(0, ARGS.m)
    values = ''
    for i in range(0, keys_in_val):
        # if we are not in the maximum nesting depth
        # generate a nested key value entry with 70% chance
        if lvl != 0 and random.uniform(0, 1) >= 0.7:
            val = generate_key_val(lvl - 1, key_dict)
        else:
            # generate a simple "key" : value entry
            # with no nested entries in value
            keys_list = list(key_dict.keys())
            r = random.randint(0, len(keys_list) - 1)
            inner_key = '"' + keys_list[r] + '"'
            val = generate_value(key_dict[keys_list[r]])
            val = f'{inner_key} : {val}'
        if i == keys_in_val - 1:
            values = values + str(val)
        else:
            values = values + str(val) + ' ; '

    if values == '':
        values = '{}'
    else:
        values = '{ ' + values + ' }'

    key_str = '"' + key_str + '"'

    return f'{key_str} : {str(values)}'


def generate_value(val_type):
    if val_type == 'string':
        return '"' + gen_random_string(ARGS.l) + '"'
    elif val_type == 'int':
        return random.randint(1, 1000)
    else:
        return round(random.uniform(1, 1000), 2)


def gen_random_string(max_len):
    length = random.randint(1, max_len)
    rand_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return rand_str


def generate_file(n_lines, key_dict):
    f = open("./dataToIndex.txt", "w")
    for i in range(0, n_lines):
        line = generate_key_val(ARGS.d, key_dict, i)
        assert check_syntax(line) is True
        f.write(f'{line}\n')
    f.close()
    return


def parse_key_file(filename):
    key_dict = {}
    f = open(filename, "r")
    for ln in f.readlines():
        ln = ln.rstrip()
        key_name, key_type = ln.split()
        key_dict[key_name] = key_type
        print(key_name, key_type)
    f.close()
    return key_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', type=str, default='keyFile.txt', help='Key file location')
    parser.add_argument('-n', type=int, default=10000, help='Number of lines to generate')
    parser.add_argument('-d', type=int, default=3, help='Maximum level of nesting')
    parser.add_argument('-m', type=int, default=4, help='Maximum level of keys inside value')
    parser.add_argument('-l', type=int, default=8, help='Maximum string length')
    ARGS = parser.parse_args()
    key_dict = parse_key_file(ARGS.k)
    generate_file(ARGS.n, key_dict)
