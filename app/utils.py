from passlib.context import CryptContext

pwd_cntxt =  CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_pwd(password: str):
    return pwd_cntxt.hash(password)

def pass_verify(plain_pass: str, hash_pass: str):
    return pwd_cntxt.verify(plain_pass,hash_pass)