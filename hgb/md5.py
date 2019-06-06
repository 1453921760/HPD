import hashlib

def md5_encode(a):
    m2 = hashlib.md5()   
    m2.update(a.encode('utf-8'))   
    return  m2.hexdigest()

