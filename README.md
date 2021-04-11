# README - Alexandros Kalimeris - ds1200003

## Instructions for execution:

### Important: python 3.6 or higher is needed !

In the instructions below all command line arguements are examples. You can use appropriate alternatives as you see fit.

1. Use createData.py to create data that will be used in the following steps. If you already have a file with data this step can be skipped. To run createData.py and generate data run:
    ```python3 createData.py -k keyFile.txt -n 1000 -d 3 -l 4 -m 5```

2. Start up the KV Servers by running the following commands in different terminals each:
    ```python3 kvServer.py -a 127.0.0.1 -p 65432```
    ```python3 kvServer.py -a 127.0.0.1 -p 65431```
    ```python3 kvServer.py -a 127.0.0.1 -p 65430```
    Make sure that the ip's and ports used are included in the serverFile.
3. Start up the KV broker by running in a separate terminal:
    ```python3 kvBroker.py -s serverFile.txt -i dataToIndex.txt -k 2```

4. Execute any request using the command line, some examples: . 

    A GET request:
    ``` 
    kv_broker->: GET "key1"
    "key1" : { "weight" : 302.02 ; "surname" : "free" ; "city" : "psrnt" }
    kv_broker->:
    ```
    A GET request for a non-existing key:
    ``` 
    kv_broker->: GET "asdf"
    NOT FOUND
    kv_broker->:
    ```
    A QUERY request:
    ```
    kv_broker->: QUERY "key1"."weight"
    "key1"."weight" : 302.02
    kv_broker->:
    ```
    An unknown command:
    ```
    kv_broker->: sadf
    ERROR: Unknown command
    kv_broker->:
    ```
    A request with an empty body:
    ```
    kv_broker->: GET
    ERROR: Syntax error in request
    kv_broker->:
    ```


5. Exit the KV broker either by typing 'exit' or ctrl-C:
    ```
    kv_broker->: exit
    ```
6. Close the KV servers by using ctrl-C.