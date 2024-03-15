import hashlib
from app import *
import snowflake.connector


def encrypt(vendor_pwd):
    
    vendor_pwd_raw = hashlib.md5(vendor_pwd.encode())
    vendor_pwd_enc = vendor_pwd_raw.hexdigest()
    return vendor_pwd_enc

def decryption(s):
    s=0
    return s

def debug_table(curs):
    query_id = curs.sfqid
    curs.get_results_from_sfqid(query_id)
    results = curs.fetchall()
    return results

def read_table():
    pass
