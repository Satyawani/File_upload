# service_function.py

import time

def my_service_function():
    while True:
        with open('output.txt', 'a') as file:
            file.write('Service is running...\n')
        time.sleep(5)


def sydbconn(passwd_sy):
    host = f"04M{br_code}{passwd_sy[1]}_RO"
    print(host)
    database = f"04M{br_code}{passwd_sy[1]}_RO"
    username = "dba"
    password = passwd_sy[0]
    print(host,password)
    cs = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (host, username, password, database)
    conn = pyodbc.connect(cs)
    cur = conn.cursor()
    return conn, cur
