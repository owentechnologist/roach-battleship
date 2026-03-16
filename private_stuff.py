from connection_stuff import *
# note that the details for your connections to the database and LLM etc, will be found in the file connection_stuff.py
# by storing this info in a separate file and including that file in the .gitignore file there is less security risk
# connection_stuff.py will look like this 
'''
# import driver for CRDB/postgres:
from psycopg_pool import ConnectionPool
import os


### CRDB connection setup ###
# Q: whare is the database? A: we assume a locally hosted insecure CRDB instance

db_config = {
    'host': 'localhost',
    'port': 26257,
    'dbname': 'vdb',
    'user': 'root'
}

# to utilize certs set the env variable SECURE_CRDB=true
# SECURE_CRDB=true
CERTDIR = '/Users/owentaylor/.cockroach-certs'
db_config_secure = {
    'host': 'localhost',
    'port': 26257,
    'dbname': 'vdb',
    'user': 'root',
    # SSL parameters:
    'sslmode': 'verify-full',         # or 'verify-full' if your host matches the cert SAN
    'sslrootcert': f'{CERTDIR}/ca.crt',
    'sslcert': f'{CERTDIR}/client.root.crt',
    'sslkey': f'{CERTDIR}/client.root.key',
    'connect_timeout': 10,
}

CERTDIR = f"{os.environ['HOME']}/Library/Company/certs/test"
db_config_secure = {
    'host': 'region-demo.us-west.cockroachlabz.cloud',
    'port': 26257,
    'dbname': 'vdb',
    'user': 'disruptor',
    'password': '9l5Ui1GoA2ssw2aaS3-Ln-3-w',        # SSL parameters:
    'sslmode': 'verify-full',         # or 'verify-full' if your host matches the cert SAN
    'sslrootcert': f'{CERTDIR}/region-demo-myCA.crt',
    'connect_timeout': 10,
}

# Initialize pool as None so it persists between function calls
_pool = None


# here is where we test for the env variable SECURE_CRDB and return connections:
def get_connection():
    global _pool
    if _pool is None:
        if(os.getenv("SECURE_CRDB", "false")=='true'):
            print('GETTING SECURE CONNECTION...')
            _pool = ConnectionPool(conninfo="",**db_config_secure)
        else:
            print('GETTING NON-SECURE (PLAIN) CONNECTION...')
            _pool = ConnectionPool(conninfo=db_url)
        # use unpacking operator ** to turn dict to separate args:
    connection = _pool.connection() 
        
    assert connection is not None, "get_connection() returned None (connection failed)"
    return connection

def close_pool():
    global _pool
    if _pool is not None:
        _pool.close()
        print("Connection pool closed.")
    
'''