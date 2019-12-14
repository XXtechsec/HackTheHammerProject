import os
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC

def register():
    key = ECC.generate(curve="P-256")
    return key

def get_message():
    return os.urandom(64)

def get_priv_key(key):
    return key.export_key(format='PEM')

def get_publ_key(key):
    return key.public_key().export_key(format='PEM')

def get_signature(message, pk):
    h = SHA256.new(message)
    key = ECC.import_key(pk)
    signer = DSS.new(key, "fips-186-3")
    return signer.sign(h)

def verify_signature(message, sig, pk):
    h = SHA256.new(message)
    key = ECC.import_key(pk)
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h, sig)
        print("Valid!")
    except ValueError:
        print("Invalid!")
